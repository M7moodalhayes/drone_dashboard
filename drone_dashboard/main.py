import asyncio
import threading
import customtkinter as ctk
from dashboard import DroneDashboard
from drone_controller import DroneController

class DroneApp:
    def __init__(self):
        # Use soft dark theme like Apple Dark Mode
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main window
        self.root = ctk.CTk()
        self.root.title("Drone Control Dashboard")
        self.root.geometry("1200x800")
        
        # Initialize drone controller
        self.drone_controller = DroneController()
        
        # Initialize dashboard
        self.dashboard = DroneDashboard(self.root, self.drone_controller)
        
        # Start async loop in separate thread
        self.async_thread = threading.Thread(target=self.run_async_loop, daemon=True)
        self.async_thread.start()
    
    def run_async_loop(self):
        """Run asyncio loop in separate thread"""
        try:
            self.drone_controller.loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self.drone_controller.loop)
            self.drone_controller.loop.run_until_complete(self.drone_controller.connect())
            self.drone_controller.loop.run_forever()
        except Exception as e:
            print(f"❌ Async loop error: {e}")
    
    def run(self):
        """Start the application"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"❌ GUI error: {e}")

if __name__ == "__main__":
    app = DroneApp()
    app.run()