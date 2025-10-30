# drone_dashboard
his project is a **real-time drone control dashboard** built with **Python**, **CustomTkinter**, and **MAVSDK**.  
It provides a modern, Apple-style dark interface to monitor and control MAVLink-based drones such as PX4 or ArduPilot.

The system allows you to **connect**, **arm**, **take off**, **land**, and manually control **throttle**, **yaw**, **pitch**, and **roll**, while displaying live telemetry — GPS position, altitude, attitude, and battery level — in real time.  
An elegant attitude indicator visualizes roll and pitch dynamically, and a **mock test mode** is included for running the full interface without a real drone connected.

The architecture cleanly separates GUI (`dashboard.py`) and drone logic (`drone_controller.py`), combining **asyncio** concurrency with **CustomTkinter’s** smooth interface for fast, stable performance.  
It’s designed for **robotics, UAV research**, and **Teknofest-style competitions**, making it an excellent base for advanced drone projects or autonomous flight experimentation.

---

### 🧩 Features
- Real-time telemetry updates (GPS, attitude, battery)
- Full MAVSDK integration for PX4/SITL or real drones
- Manual RC-like control sliders for flight axes
- Apple-inspired dark UI theme with responsive cards
- Mock mode for development without hardware
- Clean async + multithreaded architecture

---

### ⚙️ Quick Start
```bash
# Clone the repository
git clone https://github.com/<your-username>/ai_vision_app.git
cd ai_vision_app

# Install dependencies
pip install -r requirements.txt

# Run mock mode (no drone required)
python mock_ui_test.py

# Or run full dashboard (requires MAVSDK running)
python main.py 
