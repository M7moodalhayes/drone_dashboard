import asyncio
from mavsdk import System
from mavsdk.offboard import (OffboardError, VelocityBodyYawspeed, PositionNedYaw)
import math

class DroneController:
    def __init__(self):
        self.drone = System()
        self.connected = False
        self.in_air = False
        self.armed = False
        self.loop = None
        self.offboard_started = False
        self.manual_offboard_override = False
        
        # Control parameters
        self.throttle = 0.0
        self.yaw = 0.0
        self.pitch = 0.0
        self.roll = 0.0
        
        # Position and attitude info
        self.position = (0, 0, 0)
        self.attitude = (0, 0, 0)
        self.battery = 0.0
        self.gps_fix = 0
        
    async def connect(self, connection_string="udp://:14540"):
        """Connect to the drone"""
        print(f"🔗 Connecting to drone: {connection_string}")
        
        try:
            await self.drone.connect(system_address=connection_string)
            
            # Wait for connection
            print("⏳ Waiting for drone connection...")
            async for state in self.drone.core.connection_state():
                if state.is_connected:
                    print("✅ Connected to drone!")
                    self.connected = True
                    break
            
            # Start status monitoring
            asyncio.create_task(self.monitor_status())
            asyncio.create_task(self.monitor_position())
            asyncio.create_task(self.monitor_attitude_enhanced())  # Enhanced attitude monitoring
            asyncio.create_task(self.monitor_battery())
            asyncio.create_task(self.monitor_gps())
            
            print("📊 Enhanced status monitoring started")
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
    
    async def monitor_status(self):
        """Monitor drone status"""
        async for is_armed in self.drone.telemetry.armed():
            self.armed = is_armed
        
        async for is_in_air in self.drone.telemetry.in_air():
            old_state = self.in_air
            self.in_air = is_in_air
            
            if is_in_air and not old_state:
                print("🛫 Drone is now IN AIR - RC controls can be used!")
                await self.start_offboard_mode()
            elif not is_in_air and old_state:
                print("🛬 Drone has LANDED - RC controls disabled")
            
            if not is_in_air and self.offboard_started:
                await self.stop_offboard_mode()
    
    async def monitor_position(self):
        """Monitor drone position"""
        async for position in self.drone.telemetry.position():
            self.position = (position.latitude_deg, position.longitude_deg, 
                           position.relative_altitude_m)
    
    async def monitor_attitude_enhanced(self):
        """Enhanced attitude monitoring with better data handling"""
        print("🎯 Starting enhanced attitude monitoring...")
        
        last_print_time = asyncio.get_event_loop().time()
        print_interval = 2.0  # Print every 2 seconds
        
        async for attitude in self.drone.telemetry.attitude_euler():
            current_time = asyncio.get_event_loop().time()
            
            # Convert to degrees
            roll_deg = math.degrees(attitude.roll_rad)
            pitch_deg = math.degrees(attitude.pitch_rad) 
            yaw_deg = math.degrees(attitude.yaw_rad)
            
            # Update attitude
            self.attitude = (roll_deg, pitch_deg, yaw_deg)
            
            # Print periodically for debugging
            if current_time - last_print_time >= print_interval:
                print(f"📊 Attitude - Roll: {roll_deg:6.1f}°, Pitch: {pitch_deg:6.1f}°, Yaw: {yaw_deg:6.1f}°")
                last_print_time = current_time
                
                # Also print if we have significant movement
                if abs(roll_deg) > 10 or abs(pitch_deg) > 10:
                    print(f"🎢 Significant movement detected!")
    
    async def monitor_battery(self):
        """Monitor battery status"""
        async for battery in self.drone.telemetry.battery():
            self.battery = battery.remaining_percent * 100
    
    async def monitor_gps(self):
        """Monitor GPS status"""
        async for gps_info in self.drone.telemetry.gps_info():
            old_fix = self.gps_fix
            self.gps_fix = gps_info.fix_type.value
            
            if self.gps_fix != old_fix:
                fix_names = {0: "No GPS", 1: "No Fix", 2: "2D Fix", 3: "3D Fix", 4: "DGPS", 5: "RTK Float", 6: "RTK Fixed"}
                fix_name = fix_names.get(self.gps_fix, f"Unknown ({self.gps_fix})")
                print(f"🛰️ GPS status: {fix_name} ({gps_info.num_satellites} satellites)")
    
    async def arm(self):
        """Arm the drone"""
        print("🟡 Attempting to arm...")
        if not self.connected:
            print("❌ Not connected to drone")
            return False
        
        try:
            await self.drone.action.arm()
            print("✅ Drone armed successfully!")
            return True
        except Exception as e:
            print(f"❌ Arming failed: {e}")
            return False
    
    async def disarm(self):
        """Disarm the drone"""
        print("🟡 Attempting to disarm...")
        try:
            if self.offboard_started:
                await self.stop_offboard_mode()
            await self.drone.action.disarm()
            print("✅ Drone disarmed successfully!")
            return True
        except Exception as e:
            print(f"❌ Disarming failed: {e}")
            return False
    
    async def takeoff(self):
        """Takeoff to 5 meters - Enhanced version"""
        print("🚀 Attempting takeoff...")
        
        if not self.armed:
            print("🟡 Drone not armed, arming first...")
            armed = await self.arm()
            if not armed:
                return False
        
        try:
            await self.drone.action.set_takeoff_altitude(5.0)
            await self.drone.action.takeoff()
            print("✅ Takeoff command sent successfully!")
            
            # Wait for takeoff
            await asyncio.sleep(8)
            
            # If still not in air but at altitude, override
            if not self.in_air and self.position[2] > 2.0:
                print("🔄 Overriding in_air status (high altitude detected)")
                self.in_air = True
                await self.start_offboard_mode()
                return True
                
            return self.in_air
            
        except Exception as e:
            print(f"❌ Takeoff failed: {e}")
            return False
    
    async def land(self):
        """Land the drone"""
        print("🛬 Attempting to land...")
        try:
            if self.offboard_started:
                await self.stop_offboard_mode()
            await self.drone.action.land()
            print("✅ Land command sent successfully!")
            return True
        except Exception as e:
            print(f"❌ Landing failed: {e}")
            return False
    
    async def start_offboard_mode(self):
        """Start offboard mode for RC controls"""
        if self.offboard_started:
            return True
            
        print("🟡 Starting offboard mode for RC controls...")
        try:
            await self.drone.offboard.set_velocity_body(VelocityBodyYawspeed(0, 0, 0, 0))
            await self.drone.offboard.start()
            print("✅ Offboard mode started successfully!")
            print("🎮 RC CONTROLS ARE NOW ACTIVE - Move the sliders!")
            self.offboard_started = True
            return True
        except OffboardError as e:
            print(f"❌ Failed to start offboard mode: {e}")
            return False
    
    async def stop_offboard_mode(self):
        """Stop offboard mode"""
        if not self.offboard_started:
            return True
            
        try:
            await self.drone.offboard.stop()
            print("✅ Offboard mode stopped")
            self.offboard_started = False
            return True
        except OffboardError as e:
            print(f"❌ Failed to stop offboard mode: {e}")
            return False
    
    async def manual_takeoff_override(self):
        """Manual override for takeoff detection"""
        print("🔄 Manual takeoff override activated!")
        if self.position[2] > 2.0:
            print(f"🎯 Overriding in_air status (altitude: {self.position[2]:.1f}m)")
            self.in_air = True
            await self.start_offboard_mode()
            return True
        else:
            print("❌ Cannot override - altitude too low")
            return False
    
    async def quick_fix_offboard(self):
        """Quick fix for current situation"""
        print("🔧 Applying quick fix for offboard mode...")
        try:
            await self.drone.offboard.set_velocity_body(VelocityBodyYawspeed(0, 0, 0, 0))
            await self.drone.offboard.start()
            print("✅ Offboard mode started!")
            self.offboard_started = True
            self.in_air = True
            return True
        except Exception as e:
            print(f"❌ Quick fix failed: {e}")
            return False
    
    async def test_gyroscope(self):
        """Test method to verify gyroscope data"""
        print("🧪 Testing gyroscope data...")
        
        try:
            # Get a single attitude reading
            async for attitude in self.drone.telemetry.attitude_euler():
                roll_deg = math.degrees(attitude.roll_rad)
                pitch_deg = math.degrees(attitude.pitch_rad)
                yaw_deg = math.degrees(attitude.yaw_rad)
                
                print(f"🧭 Gyro Test - Roll: {roll_deg:.1f}°, Pitch: {pitch_deg:.1f}°, Yaw: {yaw_deg:.1f}°")
                break  # Just get one reading
                
            return True
        except Exception as e:
            print(f"❌ Gyroscope test failed: {e}")
            return False
    
    async def set_rc_controls(self):
        """Set RC-like controls using offboard mode"""
        if not self.in_air:
            return
        
        if not self.offboard_started:
            success = await self.start_offboard_mode()
            if not success:
                return
    
        try:
            forward_velocity = self.pitch * 3.0
            right_velocity = self.roll * 3.0
            down_velocity = -self.throttle * 2.0
            yaw_speed = self.yaw * 60.0
            
            if any([abs(forward_velocity) > 0.1, abs(right_velocity) > 0.1, 
                    abs(down_velocity) > 0.1, abs(yaw_speed) > 1.0]):
                print(f"🎮 RC Controls - Fwd: {forward_velocity:.1f}m/s, Right: {right_velocity:.1f}m/s, Down: {down_velocity:.1f}m/s, Yaw: {yaw_speed:.1f}°/s")
            
            velocity_command = VelocityBodyYawspeed(
                forward_m_s=forward_velocity,
                right_m_s=right_velocity,
                down_m_s=down_velocity,
                yawspeed_deg_s=yaw_speed
            )
            
            await self.drone.offboard.set_velocity_body(velocity_command)
            
        except Exception as e:
            print(f"❌ Control command failed: {e}")
    
    def update_controls(self, throttle=0, yaw=0, pitch=0, roll=0):
        """Update control inputs from GUI"""
        self.throttle = max(-1.0, min(1.0, throttle))
        self.yaw = max(-1.0, min(1.0, yaw))
        self.pitch = max(-1.0, min(1.0, pitch))
        self.roll = max(-1.0, min(1.0, roll))
        
        if self.in_air:
            asyncio.run_coroutine_threadsafe(self.set_rc_controls(), self.loop)