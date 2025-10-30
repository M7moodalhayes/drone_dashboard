import asyncio
import tkinter as tk
from tkinter import ttk

# ✅ Mock Drone Controller (so UI works without real drone)
class MockDrone:
    def __init__(self):
        self.connected = True
        self.armed = False
        self.battery = 87
        self.position = (12.34, 56.78, 30.0)
        self.attitude = (0.0, 0.0, 90.0)

    async def arm(self):
        self.armed = True

    async def takeoff(self):
        pass

    async def land(self):
        pass

    async def disarm(self):
        self.armed = False

    async def update_controls(self, *args, **kwargs):
        pass

# ✅ Basic UI
class DroneUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🚁 Drone Controller UI (Mock Mode)")
        self.drone = MockDrone()

        # --- Header ---
        header = ttk.Label(root, text="Drone Control Panel", font=("Segoe UI", 18, "bold"))
        header.pack(pady=10)

        # --- Status ---
        self.status_label = ttk.Label(root, text=self.get_status_text(), font=("Segoe UI", 12))
        self.status_label.pack(pady=5)

        # --- Buttons ---
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Arm", command=lambda: asyncio.create_task(self.arm_drone())).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Takeoff", command=lambda: asyncio.create_task(self.takeoff())).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Land", command=lambda: asyncio.create_task(self.land())).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Disarm", command=lambda: asyncio.create_task(self.disarm_drone())).pack(side=tk.LEFT, padx=5)

        # --- Live update ---
        self.update_ui()

    def get_status_text(self):
        return f"Connected: {self.drone.connected} | Armed: {self.drone.armed} | Battery: {self.drone.battery}%"

    def update_ui(self):
        self.status_label.config(text=self.get_status_text())
        self.root.after(1000, self.update_ui)

    async def arm_drone(self):
        await self.drone.arm()

    async def takeoff(self):
        await self.drone.takeoff()

    async def land(self):
        await self.drone.land()

    async def disarm_drone(self):
        await self.drone.disarm()

# --- Run App ---
if __name__ == "__main__":
    root = tk.Tk()
    style = ttk.Style()
    style.theme_use("clam")  # modern theme
    app = DroneUI(root)
    root.mainloop()
