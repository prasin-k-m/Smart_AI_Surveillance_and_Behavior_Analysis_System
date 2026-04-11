# 🚀 SmartEye: AI Surveillance & Behavior Analysis System

![Python](https://img.shields.io/badge/Python-3.9-blue)
![YOLOv8](https://img.shields.io/badge/YOLOv8n-Ultralytics-red)
![Streamlit](https://img.shields.io/badge/Dashboard-Streamlit-orange)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Active%20Development-yellow)

---

## 📌 Overview

SmartEye is an AI-powered intelligent surveillance system designed to detect threats, analyze human behavior, identify individuals, and generate real-time alerts.

This project represents my journey into building a complete end-to-end AI system, integrating multiple AI components into a real-time decision-making pipeline.

The system combines:
- Object Detection (YOLOv8n)
- Pose Analysis (MediaPipe)
- Face Recognition
- Context-Aware Risk Engine
- Telegram Alert System
- RAG-based AI Chatbot (TinyLlama)

---

## 🎯 Problem Statement

Traditional surveillance systems:
- Passively record footage
- Require manual monitoring
- Lack real-time intelligence

SmartEye transforms surveillance into an intelligent system by enabling:
- Automated threat detection
- Behavior-based understanding
- Real-time alerting and querying

---

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

---

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

---

## 🧠 AI Models Used

### 1. Person Detection
- YOLOv8n (nano) pretrained model
- Real-time tracking

### 2. Weapon Detection
Custom-trained YOLOv8n model with classes:
- Gun
- Knife

**Testing:**
The custom weapon detection model was validated using two methods:
- A publicly available video of a person threatening a shopkeeper with a gun
- A real knife tested live via webcam at home to verify real-world detection capability

### 3. Pose Detection
Using MediaPipe Pose:
- 🧍 Standing
- 🧍‍♂️ Fallen (Emergency detection)

### 4. Face Recognition
Face embeddings matched against known database. Detects:
- Known individuals
- Unknown persons

### 5. RAG-based AI Chatbot
Built using SQLite database and TinyLlama via Ollama (runs fully locally).

Example queries:
- "Any weapon detected today?"
- "Show recent alerts"
- "Was there any emergency?"

---

## ⚠️ Risk Assessment Engine

SmartEye uses a lightweight rule-based system for real-time classification.

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

---

## 🚨 Alert System (Telegram)

Real-time alerts are sent via Telegram bot.

**Example Alerts:**

```
🚨 ALERT: HIGH
👤 Person: Unknown
🧍 Posture: STANDING
🔫 Armed: YES
🕒 Time: 2026-03-04 12:31:22
```
