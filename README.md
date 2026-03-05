# **Smart AI Surveillance & Behavior Analysis System**

### **Project Status:** Active Development

This system is currently under development. New features and optimizations are being added continuously.

## **Description**

An **AI-powered intelligent surveillance system** that detects **weapons, analyzes human behavior, identifies individuals, and assesses threat levels in real time** using computer vision and deep learning.

This project integrates **YOLO object detection, MediaPipe pose estimation, and face recognition** into a unified pipeline capable of generating **real-time alerts, risk assessments, and incident logs**.

## **Key Features**

- **Person Detection & Tracking** (YOLOv8)
- **Custom Weapon Detection Model** (Gun / Knife detection)
- **Human Behavior Analysis** using MediaPipe Pose
- **Face Recognition for Identity Verification**
- **Risk Scoring Engine** (Low → Critical)
- **Real-time Alert System**
- **Incident Snapshot Capture**
- **Event Logging with Timestamp**
- **Security Monitoring Dashboard**
- **Modular Architecture for Production Deployment**

## **System Architecture**

<img width="1625" height="1683" alt="mermaid-diagram" src="https://github.com/user-attachments/assets/f7be43a1-0170-4451-953b-e62975e4d953" />

## **Technologies Used**

| Technology       | Purpose                   |
| ---------------- | ------------------------- |
| Python           | Core Programming Language |
| YOLOv8           | Object Detection          |
| MediaPipe        | Pose Estimation           |
| Face Recognition | Identity Verification     |
| OpenCV           | Video Processing          |
| Streamlit        | Monitoring Dashboard      |
| Flask            | Alert API Server          |
| NumPy            | Numerical Computation     |

## **Project Structure**

```
Smart_AI_Surveillance_System/
│
├── api/
│   └── alert_server.py
│
├── dashboard/
│   └── dashboard.py
│
├── modules/
│   ├── detection.py
│   ├── pose_analysis.py
│   ├── face_recognition_module.py
│   ├── risk_engine.py
│   └── logger.py
│
├── models/
│   ├── weapon_model.pt
│   └── yolov8n-face.pt
│
├── known_faces/
│   ├── john.jpg
│   └── alice.jpg
│
├── testing_samples/
│   └── sample_video.mp4
│
├── Output_samples/
│   └── demo_surveillance.mp4
│
├── incidents/
│   └── captured_alert_images/
│
├── main.py
├── requirements.txt
├── weapon.yaml
├── event_log.csv
└── README.md
```
## **AI Models Used**

#### 1.Person Detection

Pretrained **YOLOv8 model** used to detect and track people.

#### 2.Weapon Detection

Custom YOLO model trained on a dataset containing:

   - Guns

   - Knives

Training performed using **Ultralytics YOLOv8 framework**.

#### 3.Pose Detection

MediaPipe Pose is used to detect posture states:

   - Standing

   - Hands Raised

   - Fallen Person

#### 4.Face Recognition

Face embeddings are extracted and matched against a **known identity database**.

## **Risk Assessment Logic**

The system computes a risk score using multiple signals.

| Condition       | Risk Points |
| --------------- | ----------- |
| Weapon detected | +5          |
| Unknown person  | +2          |
| Hands raised    | +3          |
| Fallen posture  | +2          |

Risk levels:
```
0–2   → LOW
3–4   → MEDIUM
5–7   → HIGH
8+    → CRITICAL
```

Alerts are triggered when risk level reaches **HIGH or CRITICAL**.

## **Event Logging**

Every alert is recorded with a timestamp:
```
Timestamp | TrackID | Name | Posture | Armed | RiskLevel
```
Example log:
```
2026-03-04 12:31:22 | ID 3 | Unknown | HANDS UP | True | CRITICAL
```
Logs are stored in:
```
event_log.csv
```
## **Incident Capture**

When a high-risk event occurs, the system automatically stores a snapshot:
```
incidents/
   incident_3_20260304_123122.jpg
```
These images can be reviewed by security personnel.

## **Alert API**

The system can send alerts to an external monitoring server.

Example API payload:
```
{
  "track_id": 3,
  "name": "Unknown",
  "posture": "HANDS UP",
  "armed": true,
  "risk": "CRITICAL"
}
```
## **Dashboard**

A **Streamlit dashboard** provides real-time monitoring:

Displays:

   - Recent alerts

   - Event logs

   - Captured incidents

   - System activity

Run dashboard:
```
streamlit run dashboard/dashboard.py
```

## **Installation**

Clone repository:
```
git clone https://github.com/yourusername/Smart_AI_Surveillance_System.git
cd Smart_AI_Surveillance_System
```

Install dependencies:
```
pip install -r requirements.txt
```

## **Run the System**

Run the surveillance pipeline:
```
python main.py
```
Run alert server:
```
python api/alert_server.py
```
Run dashboard:
```
streamlit run dashboard/dashboard.py
```

## **Example Results**

Input Video:
```
testing_samples/sample_video.mp4
```
Output Detection:
```
Output_samples/demo_surveillance.mp4
```
Detected events:

- Weapon detected

- Person identified

- Risk level evaluated

- Alert triggered

## **Applications**

This system can be applied in:

- Airports

- Railway stations

- Shopping malls

- Public events

- Smart city surveillance

- Security monitoring centers

## **Ethical Considerations**

This system is intended for **research and security assistance only**.

Deployment must comply with:

- Local privacy regulations

- Data protection laws

- Ethical AI practices

Human oversight is required before taking real-world actions.

## **Author**

**Prasin K M**

Data Science Intern | AI & Computer Vision Enthusiast

## **Future Improvements**

- Multi-camera surveillance support

- Edge deployment with GPU acceleration

- Crowd behavior analysis

- Real-time threat heatmaps

- Cloud-based alert system

## **If you found this project useful**

Please consider **starring the repository**.
