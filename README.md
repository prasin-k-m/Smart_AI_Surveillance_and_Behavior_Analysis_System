SmartEye — AI Surveillance & Behavior Analysis System

An end-to-end intelligent surveillance pipeline combining object detection, pose estimation, face recognition, and real-time alerting into a single modular system.

Show Image Show Image Show Image Show Image Show Image

Table of Contents

Overview
Problem Statement
Key Features
System Architecture
Tech Stack
AI Models
Risk Assessment Engine
Alert System
Dashboard
Project Structure
Prerequisites
Installation
Configuration
Usage
Applications
Roadmap
Ethical Considerations
Author
License


Overview
SmartEye transforms passive CCTV footage into an active, intelligent monitoring system. It combines multiple AI components into a real-time decision-making pipeline — detecting threats, analyzing human behavior, identifying individuals, and dispatching alerts automatically.
Core pipeline:
Video Input → Person Detection → Pose & Face Analysis → Risk Assessment → Alert + Logging

Problem Statement
Traditional surveillance systems record footage passively, require constant manual monitoring, and provide no real-time intelligence. SmartEye addresses this by enabling:

Automated, rule-based threat detection
Behavior-based scene understanding (armed, fallen, unknown)
Instant alerting via Telegram with structured event data
Natural language querying of surveillance history via a RAG chatbot


Key Features
FeatureDescriptionPerson Detection & TrackingYOLOv8 detects and tracks individuals across framesWeapon DetectionCustom-trained YOLOv8 model for guns and knivesBehavior AnalysisMediaPipe pose estimation classifies standing vs. fallenFace RecognitionMatches detected faces against a known-persons databaseRisk EngineLightweight rule-based classifier: LOW / HIGH / MEDICALTelegram AlertsReal-time structured alerts pushed via Telegram botEvent LoggingSQLite database storing all events with timestampsRAG ChatbotNatural language querying of surveillance history via OllamaStreamlit DashboardLive monitoring interface with alerts, logs, and chatbot

System Architecture
┌──────────────────────────────────────────────────────────────────┐
│                          Video Source                            │
│                     (Webcam / IP Camera)                         │
└────────────────────────────┬─────────────────────────────────────┘
                             │
                    ┌────────▼────────┐
                    │  YOLOv8 Person  │
                    │  Detection &    │
                    │  Tracking       │
                    └────────┬────────┘
                             │
          ┌──────────────────┼──────────────────┐
          │                  │                  │
 ┌────────▼────────┐ ┌───────▼───────┐ ┌───────▼───────┐
 │ Weapon Detection│ │  MediaPipe    │ │    Face       │
 │ (Custom YOLOv8) │ │  Pose (Stand/ │ │ Recognition   │
 │ Gun / Knife     │ │  Fallen)      │ │ Known/Unknown │
 └────────┬────────┘ └───────┬───────┘ └───────┬───────┘
          │                  │                  │
          └──────────────────▼──────────────────┘
                             │
                  ┌──────────▼──────────┐
                  │   Risk Assessment   │
                  │   Engine            │
                  │   LOW / HIGH /      │
                  │   MEDICAL           │
                  └──────────┬──────────┘
                             │
               ┌─────────────┼─────────────┐
               │             │             │
      ┌────────▼──────┐ ┌───▼────┐ ┌──────▼──────┐
      │ Telegram Alert│ │ SQLite │ │  Streamlit  │
      │ Bot           │ │ Logger │ │  Dashboard  │
      └───────────────┘ └────────┘ └─────────────┘

Tech Stack
TechnologyPurposePython 3.10+Core languageYOLOv8 (Ultralytics)Object and weapon detectionMediaPipePose estimationOpenCVVideo capture and frame processingface_recognitionFace embedding and identity matchingStreamlitMonitoring dashboard UITelegram Bot APIReal-time push alertsSQLitePersistent event storageOllamaLocal LLM for RAG chatbotPandasData handling and log display

AI Models
1. Person Detection & Tracking

Model: YOLOv8 pretrained (yolov8n.pt or higher)
Task: Detect and assign track IDs to people across frames
Output: Bounding boxes + track ID per detected person

2. Weapon Detection

Model: Custom YOLOv8 fine-tuned on weapon dataset (weapon.yaml)
Classes: gun, knife
Output: Per-frame detection flag with class label

3. Pose Estimation

Model: MediaPipe Pose
Classes:

STANDING — normal posture detected
FALLEN — person appears to have collapsed (emergency trigger)



4. Face Recognition

Library: face_recognition (dlib-based)
Process: Face embeddings compared against known_faces/ directory
Output: Known (with name) or Unknown

5. RAG Chatbot

Backend: SQLite (surveillance.db) + Ollama (local LLM)
Capability: Natural language queries over stored surveillance events
Example queries:

"Any weapon detected today?"
"Show recent HIGH risk events"
"Was there a medical emergency this week?"




Risk Assessment Engine
A lightweight, interpretable rule-based classifier runs on every tracked event:
pythonif any(armed_flags):
    risk = "HIGH"       # Weapon detected — security threat
elif posture == "FALLEN":
    risk = "MEDICAL"    # Person has collapsed — medical emergency
else:
    risk = "LOW"        # No threat detected
ConditionRisk LevelActionWeapon detectedHIGHTelegram alert + logPerson fallenMEDICALTelegram alert + logNo threatLOWLog only

Alert System
Alerts are dispatched instantly via a Telegram bot whenever a HIGH or MEDICAL event is detected.
HIGH risk alert:
🚨 ALERT: HIGH
👤 Person: Unknown
🧍 Posture: STANDING
🔫 Armed: YES
🕒 Time: 2026-03-04 12:31:22
MEDICAL alert:
🚑 ALERT: MEDICAL
👤 Person: Known — Prasin
🧍 Posture: FALLEN
🔫 Armed: NO
🕒 Time: 2026-03-04 12:35:10

Dashboard
The Streamlit dashboard (dashboard/app.py) provides a centralized monitoring interface:

Live Alerts — real-time HIGH/MEDICAL event feed
Event Log — searchable, filterable table of all events
System Status — camera health and model status indicators
AI Chatbot — RAG-powered natural language interface to surveillance history

Run the dashboard:
bashstreamlit run dashboard/app.py

Project Structure
Smart_AI_Surveillance_System/
│
├── app/
│   ├── alert/            # Telegram alert dispatcher
│   ├── database/         # SQLite event logging
│   ├── detection/        # YOLOv8 person + weapon detection
│   ├── face/             # Face recognition module
│   ├── pose/             # MediaPipe pose estimation
│   ├── main.py           # Main pipeline entry point
│   └── __init__.py
│
├── dashboard/
│   └── app.py            # Streamlit dashboard + RAG chatbot
│
├── rag/                  # RAG pipeline (SQLite + Ollama)
├── dataset/              # Training data
├── models/               # Saved model weights
├── known_faces/          # Reference face images for recognition
├── outputs/              # Annotated output frames/video
├── tests/                # Unit and integration tests
├── runs/                 # YOLOv8 training runs
├── sample_data/          # Sample footage for testing
│
├── surveillance.db       # SQLite event database
├── weapon.yaml           # Custom weapon detection config
├── requirements.txt
├── .env.example          # Environment variable template
├── .gitignore
└── README.md

Prerequisites
Before installing, ensure you have the following:

Python 3.10 or higher
pip (package manager)
Git
Ollama — for the local LLM chatbot (install here)
A Telegram bot token — create one via @BotFather
A webcam or IP camera accessible to OpenCV
GPU recommended — CUDA-compatible GPU significantly improves detection speed; CPU-only mode is supported but slower

Recommended hardware:

RAM: 8GB minimum, 16GB recommended
GPU: NVIDIA GTX 1060 or better (for real-time YOLO inference)


Installation
1. Clone the repository:
bashgit clone https://github.com/your-username/Smart_AI_Surveillance_System.git
cd Smart_AI_Surveillance_System
2. Create and activate a virtual environment:
bashpython -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
3. Install dependencies:
bashpip install -r requirements.txt
4. Pull the Ollama model for the chatbot:
bashollama pull llama3

Configuration
1. Copy the environment template:
bashcp .env.example .env
2. Edit .env with your credentials:
envTELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
CAMERA_INDEX=0          # 0 = default webcam; use RTSP URL for IP cameras
3. Add known faces:
Place clear, front-facing photos of known individuals into the known_faces/ directory. Name each file with the person's name:
known_faces/
├── prasin.jpg
├── john_doe.jpg
└── jane_smith.jpg

Usage
Run the main surveillance pipeline:
bashpython app/main.py
Run the monitoring dashboard:
bashstreamlit run dashboard/app.py
Run tests:
bashpytest tests/

Applications
SmartEye is designed for deployment in high-footfall or security-critical environments:

Airports and transportation hubs
Railway and bus stations
Shopping malls and retail spaces
Public events and gatherings
Smart city infrastructure


Roadmap

 YOLOv8 person detection and tracking
 Custom weapon detection (gun/knife)
 MediaPipe pose estimation (standing/fallen)
 Face recognition (known vs. unknown)
 Risk assessment engine
 Telegram real-time alerts
 SQLite event logging
 Streamlit dashboard
 RAG-based AI chatbot
 Multi-camera support
 Edge deployment (Jetson Nano / Raspberry Pi)
 Crowd behavior and density analysis
 Threat heatmaps and spatial analytics
 Cloud-based alert and storage integration
 GDPR-compliant data anonymization options


Ethical Considerations
SmartEye involves face recognition and behavioral analysis, which carry significant privacy implications. The following principles govern its intended use:

Legal compliance: Deployment must comply with applicable privacy laws in your jurisdiction (GDPR, PDPA, etc.). Surveillance of individuals without consent may be unlawful.
Informed consent: In most contexts, individuals should be notified they are being monitored. Signage is the minimum standard; explicit consent may be required.
Human oversight: This system is designed to assist human security personnel, not replace them. All HIGH and MEDICAL alerts should be reviewed by a human before action is taken.
Data minimization: Retain event data only as long as necessary. The SQLite database should be purged on a defined schedule.
No autonomous action: SmartEye does not take any physical or enforcement action. It only detects, logs, and alerts.
Bias awareness: AI-based face recognition systems can exhibit demographic bias. Accuracy should be validated for your specific deployment population before use in operational settings.


This project is intended for educational, research, and authorized security use only.


Author
Prasin K M
Data Science Intern | AI & Computer Vision Enthusiast

License
This project is licensed under the MIT License. See LICENSE for details.

If you found this project useful, consider starring the repository and sharing it with others.
