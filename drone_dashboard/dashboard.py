import asyncio
import customtkinter as ctk
import math

class DroneDashboard:
    def __init__(self, root, drone_controller):
        self.root = root
        self.drone = drone_controller
        
        # Use soft dark theme like Apple Dark Mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Apple-inspired dark color palette
        self.colors = {
            "primary": "#0A84FF",      # Apple Blue
            "success": "#30D158",      # Apple Green  
            "warning": "#FF9F0A",      # Apple Orange
            "error": "#FF453A",        # Apple Red
            "background": "#000000",   # Black
            "surface": "#1C1C1E",      # Dark Gray - Apple's dark surface
            "surface_light": "#2C2C2E", # Lighter dark for cards
            "text_primary": "#FFFFFF", # White
            "text_secondary": "#98989D", # Light Gray
            "border": "#38383A",       # Dark border
            "accent": "#BF5AF2"        # Apple Purple accent
        }
        
        # Initialize card_values dictionary
        self.card_values = {}
        
        # Configure root window
        self.root.configure(fg_color=self.colors["background"])
        self.root.title("Drone Control Dashboard")
        self.root.geometry("1200x800")
        
        # Main container
        self.main_frame = ctk.CTkFrame(self.root, fg_color=self.colors["background"], corner_radius=0)
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Grid layout
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=2)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Create UI sections
        self.create_header()
        self.create_left_panel()
        self.create_visualization_panel()
        
        # Start UI updates
        self.update_ui()
    
    def create_header(self):
        """Create simple header with soft dark theme"""
        header = ctk.CTkFrame(self.main_frame, fg_color="transparent", height=60)
        header.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        
        title = ctk.CTkLabel(header, 
                           text="Drone Control Dashboard",
                           font=("Arial", 24, "bold"),
                           text_color=self.colors["text_primary"])
        title.pack(anchor="w")
        
        subtitle = ctk.CTkLabel(header,
                              text="Real-time drone monitoring and control",
                              font=("Arial", 12),
                              text_color=self.colors["text_secondary"])
        subtitle.pack(anchor="w")
    
    def create_left_panel(self):
        """Create left panel with controls and status"""
        left_panel = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(0, 15))
        
        # Status cards
        self.create_status_cards(left_panel)
        
        # Action buttons
        self.create_action_buttons(left_panel)
        
        # RC Controls
        self.create_rc_controls(left_panel)
    
    def create_status_cards(self, parent):
        """Create status display cards with dark theme"""
        status_frame = ctk.CTkFrame(parent, fg_color="transparent")
        status_frame.pack(fill="x", pady=(0, 20))
        
        # Grid for status cards
        grid_frame = ctk.CTkFrame(status_frame, fg_color="transparent")
        grid_frame.pack(fill="x")
        grid_frame.columnconfigure(0, weight=1)
        grid_frame.columnconfigure(1, weight=1)
        
        # Connection status
        self.connection_card, conn_value = self.create_simple_card(grid_frame, "🔗 Connection", "Disconnected", self.colors["error"])
        self.connection_card.grid(row=0, column=0, padx=(0, 10), pady=(0, 10), sticky="ew")
        self.card_values["connection"] = conn_value
        
        # Armed status
        self.armed_card, armed_value = self.create_simple_card(grid_frame, "⚡ Armed", "No", self.colors["error"])
        self.armed_card.grid(row=0, column=1, padx=(10, 0), pady=(0, 10), sticky="ew")
        self.card_values["armed"] = armed_value
        
        # Flight status
        self.flight_card, flight_value = self.create_simple_card(grid_frame, "🛩️ Flight Mode", "Ground", self.colors["error"])
        self.flight_card.grid(row=1, column=0, padx=(0, 10), pady=(10, 0), sticky="ew")
        self.card_values["flight"] = flight_value
        
        # GPS status
        self.gps_card, gps_value = self.create_simple_card(grid_frame, "🛰️ GPS", "No Fix", self.colors["error"])
        self.gps_card.grid(row=1, column=1, padx=(10, 0), pady=(10, 0), sticky="ew")
        self.card_values["gps"] = gps_value
    
    def create_simple_card(self, parent, title, value, color):
        """Create a simple status card and return card + value label"""
        card = ctk.CTkFrame(parent, 
                          fg_color=self.colors["surface_light"],
                          border_color=self.colors["border"],
                          border_width=1,
                          corner_radius=12)
        
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=15, pady=15)
        
        # Title
        title_label = ctk.CTkLabel(content, text=title, 
                                 font=("Arial", 11, "bold"),
                                 text_color=self.colors["text_secondary"])
        title_label.pack(anchor="w")
        
        # Value
        value_label = ctk.CTkLabel(content, text=value,
                                 font=("Arial", 16, "bold"),
                                 text_color=color)
        value_label.pack(anchor="w", pady=(5, 0))
        
        return card, value_label
    
    def create_action_buttons(self, parent):
        """Create action buttons with dark theme"""
        actions_frame = ctk.CTkFrame(parent, 
                                   fg_color=self.colors["surface_light"],
                                   border_color=self.colors["border"], 
                                   border_width=1,
                                   corner_radius=12)
        actions_frame.pack(fill="x", pady=(0, 20))
        
        content = ctk.CTkFrame(actions_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(content, text="🚀 Flight Actions",
                   font=("Arial", 16, "bold"),
                   text_color=self.colors["text_primary"]).pack(anchor="w", pady=(0, 15))
        
        # Buttons grid
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(fill="x")
        btn_frame.columnconfigure(0, weight=1)
        btn_frame.columnconfigure(1, weight=1)
        
        # ARM button
        self.arm_btn = ctk.CTkButton(btn_frame, text="⚡ ARM", 
                                   command=self.arm_drone,
                                   fg_color=self.colors["success"],
                                   hover_color="#25A249",
                                   font=("Arial", 13, "bold"),
                                   height=40,
                                   corner_radius=8)
        self.arm_btn.grid(row=0, column=0, padx=(0, 8), pady=4, sticky="ew")
        
        # DISARM button
        self.disarm_btn = ctk.CTkButton(btn_frame, text="🛑 DISARM",
                                      command=self.disarm,
                                      fg_color=self.colors["error"], 
                                      hover_color="#E53E3E",
                                      font=("Arial", 13, "bold"),
                                      height=40,
                                      corner_radius=8)
        self.disarm_btn.grid(row=0, column=1, padx=(8, 0), pady=4, sticky="ew")
        
        # TAKEOFF button
        self.takeoff_btn = ctk.CTkButton(btn_frame, text="🚀 TAKEOFF",
                                       command=self.takeoff,
                                       fg_color=self.colors["primary"],
                                       hover_color="#007AFF",
                                       font=("Arial", 13, "bold"),
                                       height=40,
                                       corner_radius=8)
        self.takeoff_btn.grid(row=1, column=0, padx=(0, 8), pady=4, sticky="ew")
        
        # LAND button
        self.land_btn = ctk.CTkButton(btn_frame, text="🛬 LAND",
                                    command=self.land,
                                    fg_color=self.colors["warning"],
                                    hover_color="#E69B00",
                                    font=("Arial", 13, "bold"),
                                    height=40,
                                    corner_radius=8)
        self.land_btn.grid(row=1, column=1, padx=(8, 0), pady=4, sticky="ew")
        
        # Gyro test button
        self.gyro_test_btn = ctk.CTkButton(btn_frame, text="🧪 Test Gyro",
                                         command=self.test_gyroscope,
                                         fg_color=self.colors["accent"],
                                         hover_color="#9D4ED6",
                                         font=("Arial", 13, "bold"),
                                         height=40,
                                         corner_radius=8)
        self.gyro_test_btn.grid(row=2, column=0, columnspan=2, padx=5, pady=4, sticky="ew")
    
    def create_rc_controls(self, parent):
        """Create RC controls panel with dark theme"""
        controls_frame = ctk.CTkFrame(parent,
                                    fg_color=self.colors["surface_light"],
                                    border_color=self.colors["border"],
                                    border_width=1,
                                    corner_radius=12)
        controls_frame.pack(fill="x")
        
        content = ctk.CTkFrame(controls_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(content, text="🎮 Manual Controls",
                   font=("Arial", 16, "bold"),
                   text_color=self.colors["text_primary"]).pack(anchor="w", pady=(0, 20))
        
        # Controls grid
        controls_grid = ctk.CTkFrame(content, fg_color="transparent")
        controls_grid.pack(fill="x")
        
        # Throttle
        self.create_control_slider(controls_grid, "Throttle", 0)
        # Yaw
        self.create_control_slider(controls_grid, "Yaw", 1)
        # Pitch
        self.create_control_slider(controls_grid, "Pitch", 2) 
        # Roll
        self.create_control_slider(controls_grid, "Roll", 3)
        
        # Reset button
        reset_btn = ctk.CTkButton(content, text="🔄 Reset Controls",
                                command=self.reset_controls,
                                fg_color=self.colors["text_secondary"],
                                hover_color="#7A7A7E",
                                font=("Arial", 12, "bold"),
                                height=35,
                                corner_radius=8)
        reset_btn.pack(pady=(20, 0))
    
    def create_control_slider(self, parent, label, column):
        """Create a control slider with dark theme"""
        slider_frame = ctk.CTkFrame(parent, fg_color="transparent")
        slider_frame.grid(row=0, column=column, padx=10, sticky="ns")
        
        # Label
        ctk.CTkLabel(slider_frame, text=label,
                   font=("Arial", 12, "bold"),
                   text_color=self.colors["text_primary"]).pack(pady=(0, 10))
        
        # Value display
        value_label = ctk.CTkLabel(slider_frame, text="0%",
                                 font=("Arial", 14, "bold"),
                                 text_color=self.colors["primary"])
        value_label.pack(pady=(0, 10))
        
        # Slider
        slider = ctk.CTkSlider(slider_frame,
                              from_=-100,
                              to=100,
                              orientation="vertical", 
                              height=120,
                              width=20,
                              button_color=self.colors["primary"],
                              progress_color=self.colors["primary"],
                              button_hover_color="#007AFF",
                              fg_color=self.colors["border"])
        slider.set(0)
        slider.pack()
        
        # Store references
        if label == "Throttle":
            self.throttle_slider = slider
            self.throttle_label = value_label
            slider.configure(command=lambda v: self.on_throttle_change(v, value_label))
        elif label == "Yaw":
            self.yaw_slider = slider
            self.yaw_label = value_label
            slider.configure(command=lambda v: self.on_yaw_change(v, value_label))
        elif label == "Pitch":
            self.pitch_slider = slider
            self.pitch_label = value_label
            slider.configure(command=lambda v: self.on_pitch_change(v, value_label))
        elif label == "Roll":
            self.roll_slider = slider
            self.roll_label = value_label
            slider.configure(command=lambda v: self.on_roll_change(v, value_label))
    
    def create_visualization_panel(self):
        """Create right panel with visualization in dark theme"""
        viz_frame = ctk.CTkFrame(self.main_frame,
                               fg_color=self.colors["surface_light"],
                               border_color=self.colors["border"],
                               border_width=1,
                               corner_radius=12)
        viz_frame.grid(row=1, column=1, sticky="nsew", padx=(15, 0))
        
        content = ctk.CTkFrame(viz_frame, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        ctk.CTkLabel(content, text="📊 Flight Visualization",
                   font=("Arial", 18, "bold"),
                   text_color=self.colors["text_primary"]).pack(anchor="w", pady=(0, 20))
        
        # Attitude indicator
        att_frame = ctk.CTkFrame(content, fg_color="transparent")
        att_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        ctk.CTkLabel(att_frame, text="Attitude Indicator",
                   font=("Arial", 14, "bold"),
                   text_color=self.colors["text_secondary"]).pack(pady=(0, 10))
        
        self.canvas = ctk.CTkCanvas(att_frame, width=400, height=300, bg="#0A0A0A", highlightthickness=0)
        self.canvas.pack(pady=10)
        
        # Telemetry data
        telemetry_frame = ctk.CTkFrame(content, fg_color="transparent")
        telemetry_frame.pack(fill="x")
        
        # Position
        pos_frame = ctk.CTkFrame(telemetry_frame, fg_color="transparent")
        pos_frame.pack(fill="x", pady=5)
        
        self.lat_label = ctk.CTkLabel(pos_frame, text="Latitude: 0.000000", 
                                    font=("Arial", 12),
                                    text_color=self.colors["text_primary"])
        self.lat_label.pack(side="left", padx=(0, 20))
        
        self.lon_label = ctk.CTkLabel(pos_frame, text="Longitude: 0.000000",
                                    font=("Arial", 12),
                                    text_color=self.colors["text_primary"])
        self.lon_label.pack(side="left", padx=(0, 20))
        
        self.alt_label = ctk.CTkLabel(pos_frame, text="Altitude: 0.0 m",
                                    font=("Arial", 12),
                                    text_color=self.colors["text_primary"])
        self.alt_label.pack(side="left")
        
        # Attitude
        att_data_frame = ctk.CTkFrame(telemetry_frame, fg_color="transparent")
        att_data_frame.pack(fill="x", pady=5)
        
        self.roll_label = ctk.CTkLabel(att_data_frame, text="Roll: 0.0°",
                                     font=("Arial", 12),
                                     text_color=self.colors["text_primary"])
        self.roll_label.pack(side="left", padx=(0, 20))
        
        self.pitch_label = ctk.CTkLabel(att_data_frame, text="Pitch: 0.0°",
                                      font=("Arial", 12),
                                      text_color=self.colors["text_primary"])
        self.pitch_label.pack(side="left", padx=(0, 20))
        
        self.yaw_label = ctk.CTkLabel(att_data_frame, text="Yaw: 0.0°",
                                    font=("Arial", 12),
                                    text_color=self.colors["text_primary"])
        self.yaw_label.pack(side="left")
        
        # Battery
        battery_frame = ctk.CTkFrame(telemetry_frame, fg_color="transparent")
        battery_frame.pack(fill="x", pady=5)
        
        ctk.CTkLabel(battery_frame, text="Battery:",
                   font=("Arial", 12),
                   text_color=self.colors["text_primary"]).pack(side="left")
        
        self.battery_label = ctk.CTkLabel(battery_frame, text="0%",
                                        font=("Arial", 12, "bold"),
                                        text_color=self.colors["text_primary"])
        self.battery_label.pack(side="left", padx=(5, 0))
        
        # Status message
        self.status_label = ctk.CTkLabel(content, 
                                       text="Ready to connect",
                                       font=("Arial", 12),
                                       text_color=self.colors["text_secondary"])
        self.status_label.pack(pady=(10, 0))
    
    # Control callbacks
    def on_throttle_change(self, value, label):
        throttle = float(value) / 100.0
        label.configure(text=f"{int(value)}%")
        self.drone.update_controls(throttle=throttle)
    
    def on_yaw_change(self, value, label):
        yaw = float(value) / 100.0
        label.configure(text=f"{int(value)}%")
        self.drone.update_controls(yaw=yaw)
    
    def on_pitch_change(self, value, label):
        pitch = float(value) / 100.0
        label.configure(text=f"{int(value)}%")
        self.drone.update_controls(pitch=pitch)
    
    def on_roll_change(self, value, label):
        roll = float(value) / 100.0
        label.configure(text=f"{int(value)}%")
        self.drone.update_controls(roll=roll)
    
    def reset_controls(self):
        """Reset all controls to zero"""
        for slider in [self.throttle_slider, self.yaw_slider, self.pitch_slider, self.roll_slider]:
            slider.set(0)
        
        for label in [self.throttle_label, self.yaw_label, self.pitch_label, self.roll_label]:
            label.configure(text="0%")
        
        self.drone.update_controls(0, 0, 0, 0)
    
    # Action handlers
    def arm_drone(self):
        print("ARM button clicked")
        if self.drone.loop and self.drone.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.drone.arm(), self.drone.loop)
    
    def takeoff(self):
        print("TAKEOFF button clicked")
        if self.drone.loop and self.drone.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.drone.takeoff(), self.drone.loop)
    
    def land(self):
        print("LAND button clicked")
        if self.drone.loop and self.drone.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.drone.land(), self.drone.loop)
    
    def disarm(self):
        print("DISARM button clicked")
        if self.drone.loop and self.drone.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.drone.disarm(), self.drone.loop)
    
    def test_gyroscope(self):
        """Test gyroscope data"""
        print("🟡 GYRO TEST button clicked")
        if self.drone.loop and self.drone.loop.is_running():
            asyncio.run_coroutine_threadsafe(self.drone.test_gyroscope(), self.drone.loop)
    
    def update_ui(self):
        """Update all UI elements"""
        try:
            # Update connection status
            if self.drone.connected:
                self.card_values["connection"].configure(text="Connected", text_color=self.colors["success"])
            else:
                self.card_values["connection"].configure(text="Disconnected", text_color=self.colors["error"])
            
            # Update armed status
            if self.drone.armed:
                self.card_values["armed"].configure(text="Armed", text_color=self.colors["success"])
            else:
                self.card_values["armed"].configure(text="Disarmed", text_color=self.colors["error"])
            
            # Update flight status
            if self.drone.in_air:
                self.card_values["flight"].configure(text="In Flight", text_color=self.colors["success"])
                self.status_label.configure(text="Manual control active - Use sliders to fly")
            else:
                self.card_values["flight"].configure(text="On Ground", text_color=self.colors["text_secondary"])
                self.status_label.configure(text="Ready for takeoff")
            
            # Update GPS status
            if self.drone.gps_fix >= 3:
                self.card_values["gps"].configure(text="Good Fix", text_color=self.colors["success"])
            elif self.drone.gps_fix >= 2:
                self.card_values["gps"].configure(text="Weak Fix", text_color=self.colors["warning"])
            else:
                self.card_values["gps"].configure(text="No Fix", text_color=self.colors["error"])
            
            # Update position data
            lat, lon, alt = self.drone.position
            self.lat_label.configure(text=f"Latitude: {lat:.6f}")
            self.lon_label.configure(text=f"Longitude: {lon:.6f}")
            self.alt_label.configure(text=f"Altitude: {alt:.1f} m")
            
            # Update attitude data
            roll, pitch, yaw = self.drone.attitude
            self.roll_label.configure(text=f"Roll: {roll:.1f}°")
            self.pitch_label.configure(text=f"Pitch: {pitch:.1f}°")
            self.yaw_label.configure(text=f"Yaw: {yaw:.1f}°")
            
            # DEBUG: Print attitude values to verify they're changing
            print(f"🎯 Dashboard Attitude - Roll: {roll:.1f}°, Pitch: {pitch:.1f}°, Yaw: {yaw:.1f}°")
            
            # Update battery
            self.battery_label.configure(text=f"{self.drone.battery:.1f}%")
            
            # Update attitude indicator
            self.draw_attitude_indicator(roll, pitch)
            
        except Exception as e:
            print(f"UI update error: {e}")
        
        # Schedule next update
        self.root.after(100, self.update_ui)
    
    def draw_attitude_indicator(self, roll, pitch):
        """Fixed attitude indicator - properly displays roll and pitch"""
        canvas = self.canvas
        canvas.delete("all")
        
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            width, height = 400, 300
        
        center_x = width // 2
        center_y = height // 2
        
        # Create background
        canvas.create_rectangle(0, 0, width, height, fill="#0A0A0A", outline="")
        
        # Convert roll to radians - IMPORTANT: Negative for correct visual rotation
        roll_rad = -math.radians(roll)
        
        # Pitch scaling - adjust this value to control sensitivity
        pitch_scale = 2.5  # pixels per degree of pitch
        
        # Calculate horizon offset based on pitch
        # Positive pitch (nose up) moves horizon DOWN, negative pitch (nose down) moves horizon UP
        horizon_offset = pitch * pitch_scale
        
        # Draw sky and ground with proper rotation
        self.draw_rotated_horizon(canvas, width, height, center_x, center_y, horizon_offset, roll_rad)
        
        # Draw pitch ladder
        self.draw_pitch_ladder(canvas, width, height, center_x, center_y, horizon_offset, roll_rad, pitch_scale)
        
        # Draw fixed aircraft reference (always centered)
        self.draw_fixed_aircraft(canvas, center_x, center_y)
    
    def draw_rotated_horizon(self, canvas, width, height, center_x, center_y, horizon_offset, roll_rad):
        """Draw the rotated horizon line separating sky and ground"""
        
        # Calculate horizon line endpoints (very long line)
        line_length = max(width, height) * 2
        
        # Calculate rotated line endpoints
        x1 = center_x - line_length * math.cos(roll_rad)
        y1 = center_y + horizon_offset - line_length * math.sin(roll_rad)
        x2 = center_x + line_length * math.cos(roll_rad) 
        y2 = center_y + horizon_offset + line_length * math.sin(roll_rad)
        
        # Draw sky (above horizon)
        sky_points = [
            0, 0,                    # Top-left corner
            width, 0,                # Top-right corner  
            x2, y2,                  # Horizon right
            x1, y1,                  # Horizon left
        ]
        canvas.create_polygon(sky_points, fill="#1E3A8A", outline="")  # Dark blue sky
        
        # Draw ground (below horizon)  
        ground_points = [
            x1, y1,                  # Horizon left
            x2, y2,                  # Horizon right
            width, height,           # Bottom-right
            0, height,               # Bottom-left
        ]
        canvas.create_polygon(ground_points, fill="#78350F", outline="")  # Brown ground
        
        # Draw horizon line
        canvas.create_line(x1, y1, x2, y2, fill="#FFFFFF", width=3)
    
    def draw_pitch_ladder(self, canvas, width, height, center_x, center_y, horizon_offset, roll_rad, pitch_scale):
        """Draw pitch reference lines"""
        
        # Pitch values to display (in degrees)
        pitch_angles = [-30, -20, -10, 0, 10, 20, 30]
        
        for angle in pitch_angles:
            # Calculate line position
            line_y_offset = horizon_offset + (angle * pitch_scale)
            line_center_y = center_y + line_y_offset
            
            # Line length
            if angle == 0:
                line_length = 120  # Longer horizon line
            else:
                line_length = 80   # Shorter pitch lines
            
            # Calculate rotated line endpoints
            x1 = center_x - line_length * math.cos(roll_rad)
            y1 = line_center_y - line_length * math.sin(roll_rad)
            x2 = center_x + line_length * math.cos(roll_rad)
            y2 = line_center_y + line_length * math.sin(roll_rad)
            
            # Choose color and width
            if angle == 0:
                color = "#FFFFFF"  # White horizon
                line_width = 3
            else:
                color = "#CCCCCC"  # Gray pitch lines  
                line_width = 1
            
            # Draw the line
            canvas.create_line(x1, y1, x2, y2, fill=color, width=line_width)
            
            # Add angle labels for non-zero pitches
            if angle != 0:
                label_offset = 20
                label_x = center_x + (line_length + label_offset) * math.cos(roll_rad)
                label_y = line_center_y + (line_length + label_offset) * math.sin(roll_rad)
                
                # Only draw label if it's visible
                if 0 <= label_y <= height:
                    canvas.create_text(
                        label_x, label_y, 
                        text=str(abs(angle)) + "°", 
                        fill="#CCCCCC", 
                        font=("Arial", 10),
                        angle=math.degrees(roll_rad)  # Rotate text with horizon
                    )
    
    def draw_fixed_aircraft(self, canvas, center_x, center_y):
        """Draw the fixed aircraft reference (always centered and level)"""
        
        # Aircraft wings (horizontal)
        wing_length = 60
        wing_width = 6
        canvas.create_rectangle(
            center_x - wing_length//2, center_y - wing_width//2,
            center_x + wing_length//2, center_y + wing_width//2,
            fill="#EF4444", outline="#FFFFFF", width=2  # Red wings
        )
        
        # Aircraft body (vertical)  
        body_length = 40
        body_width = 8
        canvas.create_rectangle(
            center_x - body_width//2, center_y - body_length//2,
            center_x + body_width//2, center_y + body_length//2,
            fill="#3B82F6", outline="#FFFFFF", width=1  # Blue body
        )
        
        # Center reference dot
        canvas.create_oval(
            center_x - 6, center_y - 6,
            center_x + 6, center_y + 6,
            fill="#F59E0B", outline="#FFFFFF", width=1  # Amber center
        )
        
        # Fixed reference cross (always straight)
        cross_size = 25
        canvas.create_line(
            center_x - cross_size, center_y,
            center_x + cross_size, center_y,
            fill="#10B981", width=2, dash=(4, 2)  # Green dashed
        )
        canvas.create_line(
            center_x, center_y - cross_size,
            center_x, center_y + cross_size, 
            fill="#10B981", width=2, dash=(4, 2)  # Green dashed
        )