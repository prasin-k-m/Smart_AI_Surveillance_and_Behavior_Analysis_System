# 🚀 SmartEye: AI Surveillance & Behavior Analysis System

![Python](https://img.shields.io/badge/Python-3.9-blue) ![YOLOv8](https://img.shields.io/badge/YOLOv8n-Ultralytics-red) ![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-orange) ![License](https://img.shields.io/badge/License-MIT-green) ![Status](https://img.shields.io/badge/Status-Completed-brightgreen) ![Contributions](https://img.shields.io/badge/Contributions-Welcome-orange)
## 📌 Overview

SmartEye is an AI-powered intelligent surveillance system designed to detect threats, analyze human behavior, identify individuals, and generate real-time alerts. This project represents my journey into building a complete end-to-end AI system, integrating multiple AI components into a real-time decision-making pipeline.

The system combines Object Detection (YOLOv8n), Pose Analysis (MediaPipe), Face Recognition, a Context-Aware Risk Engine, a Telegram Alert System, and a RAG-based AI Chatbot powered by TinyLlama.

## 🎯 Problem Statement

Traditional surveillance systems passively record footage, require manual monitoring, and lack real-time intelligence. SmartEye transforms surveillance into an intelligent system by enabling automated threat detection, behavior-based understanding, and real-time alerting and querying.

## ✨ Key Features

- 👤 Person Detection & Tracking (YOLOv8n)
- 🔫 Custom Weapon Detection (Gun / Knife)
- 🧍 Human Behavior Analysis (Standing / Fallen)
- 🧠 Face Recognition (Known vs Unknown)
- ⚠️ Context-Aware Risk Engine (LOW / HIGH / MEDICAL)
- 📲 Telegram-based Real-time Alert System
- 🤖 RAG-based AI Chatbot (SQLite + TinyLlama)
- 📊 Streamlit Monitoring Dashboard
- 📝 Event Logging with Timestamp
- 🧩 Modular & Scalable Architecture

## 🛠️ Tech Stack

| Technology | Purpose |
|---|---|
| Python 3.9 | Core development |
| YOLOv8n (Ultralytics) | Object & weapon detection |
| MediaPipe | Pose estimation |
| OpenCV | Video processing |
| Face Recognition | Identity verification |
| Streamlit | Dashboard UI |
| Telegram Bot API | Real-time alerts |
| SQLite | Event storage |
| Ollama (TinyLlama) | LLM for RAG chatbot |
| Pandas | Data handling |

## 🧠 AI Models Used

### 1. Person Detection
YOLOv8n (nano) pretrained model used for real-time person tracking.

### 2. Weapon Detection
Custom-trained YOLOv8n model detecting two classes — Gun and Knife.

**Testing:** The custom weapon detection model was validated using two methods:
- A publicly available video of a person threatening a shopkeeper with a gun
- A real knife tested live via webcam to verify real-world detection capability

### 3. Pose Detection
Using MediaPipe Pose to classify:
- 🧍 Standing
- 🧍‍♂️ Fallen (Emergency detection)

### 4. Face Recognition
Face embeddings matched against a known database to detect known individuals and unknown persons.

### 5. RAG-based AI Chatbot
Built using SQLite and TinyLlama via Ollama, running fully locally.

Example queries:
- "Any weapon detected today?"
- "Show recent alerts"
- "Was there any emergency?"

## ⚠️ Risk Assessment Engine

```python
if any(armed_flags):
    risk = "HIGH"
elif posture == "FALLEN":
    risk = "MEDICAL"
else:
    risk = "LOW"
```

| Condition | Risk Level | Description |
|---|---|---|
| Weapon detected | HIGH | Security threat |
| Fallen person | MEDICAL | Medical emergency |
| No threat | LOW | Normal situation |

## 🚨 Alert System (Telegram)
🚨 ALERT: HIGH
👤 Person: Unknown
🧍 Posture: STANDING
🔫 Armed: YES
🕒 Time: 2026-03-04 12:31:22

🚑 ALERT: MEDICAL
👤 Person: Known
🧍 Posture: FALLEN
🔫 Armed: NO
🕒 Time: 2026-03-04 12:35:10

## 📊 Event Logging

All events stored in `surveillance.db` with format:
Timestamp | TrackID | Name | Posture | Armed | RiskLevel

## 📊 Dashboard (Streamlit + AI Chatbot)

Features: Live alerts, event logs, system monitoring, and RAG-powered AI chatbot.

```bash
streamlit run dashboard/app.py
```

## 📁 Project Structure
```
Smart_AI_Surveillance_System/
│
├── app/
│   ├── alert/
│   ├── database/
│   ├── detection/
│   ├── face/
│   ├── pose/
│   ├── main.py
│   └── init.py
│
├── dashboard/
│   └── app.py
│
├── rag/
├── dataset/
├── sample_data/
├── tests/
├── models/
├── runs/
├── known_faces/
├── outputs/
│
├── surveillance.db
├── weapon.yaml
├── reqiurment.txt
└── README.md
```
## ⚙️ Prerequisites

- Python 3.9
- Webcam or video file for input
- Ollama with TinyLlama ([install here](https://ollama.ai))
- Telegram bot token (create via [@BotFather](https://t.me/botfather))
- GPU recommended (CPU mode supported but slower)

## ⚙️ Installation

```bash
git clone https://github.com/prasin-k-m/Smart_AI_Surveillance_and_Behavior_Analysis_System.git
cd Smart_AI_Surveillance_and_Behavior_Analysis_System

python -m venv venv
source venv/bin/activate
# Windows: venv\Scripts\activate

pip install -r reqiurment.txt

ollama pull tinyllama
```

## ⚙️ Configuration

Create a `.env` file in the project root:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
CAMERA_INDEX=0
```

Add known face images to `known_faces/`:
```known_faces/
├── your_name.jpg
└── another_person.jpg
```
## ▶️ Run the System

Using webcam:
```bash
python app/main.py
```

Using a video file:
```bash
python app/main.py --source your_video.mp4
```

## 🌍 Applications

Airports, railway stations, shopping malls, public events, and smart city surveillance.

## 🚀 Future Improvements

- [ ] Multi-camera support
- [ ] Edge deployment
- [ ] Crowd behavior analysis
- [ ] Threat heatmaps
- [ ] Cloud-based alerts

## ⚖️ Ethical Considerations

Must comply with privacy laws. Designed for assistance, not replacement. Requires human oversight.

## 👨‍💻 Author

**Prasin K M** — Data Science Intern | AI & Computer Vision Enthusiast

GitHub: [prasin-k-m](https://github.com/prasin-k-m)

## ⭐ Support

If you found this project useful, please star the repository, share it with others, and provide feedback.
