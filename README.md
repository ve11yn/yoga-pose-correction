# 🧘‍♀️ YogaFlow AI

<div align="center">

![Project Banner](https://img.shields.io/badge/YogaFlow-AI-blue?style=for-the-badge&logo=yoga&logoColor=white)

**A Real-Time AI Yoga Instructor powered by Computer Vision**

[View Live Demo](https://yoga-pose-correction.vercel.app) · [Backend API](https://revckries-yoga-pose-backend.hf.space) · [Report Bug](https://github.com/ve11yn/yoga-pose-correction/issues)

</div>

---

## 📌 Overview

**YogaFlow AI** acts as your personal digital yoga instructor. Leveraging advanced **Computer Vision** and **Machine Learning**, it analyzes your movements in real-time through your webcam.

Unlike simple video tutorials, YogaFlow AI understands your body's geometry. It detects your pose, calculates your alignment, and provides **instant, voice-guided feedback** to help you perfect your form—just like a real teacher would.

### ✨ Key Features

- **📹 Real-Time Pose Detection**: Uses Google's MediaPipe for lightning-fast, privacy-preserving body tracking.
- **🤖 Smart Classification**: Instantly recognizes which yoga pose you are performing.
- **� Voice Coaching**: Text-to-Speech (TTS) engine gives you hands-free correction (e.g., *"Straighten your right knee!"*).
- **⏱️ Session Analytics**: Tracks potential FPS, session duration, and confidence scores.
- **� Privacy First**: All video processing happens in the browser or ephemeral containers; no video is stored.

### 🧘‍♀️ Supported Poses
| Pose | Description | Difficulty |
| :--- | :--- | :--- |
| **Downdog** | Adho Mukha Svanasana | Beginner |
| **Goddess** | Utkata Konasana | Beginner |
| **Plank** | Kumbhakasana | Intermediate |
| **Tree** | Vrksasana | Beginner |
| **Warrior II** | Virabhadrasana II | Beginner |

---

## 🧠 Under the Hood

The magic happens through a hybrid AI approach:

1.  **Pose Extraction (MediaPipe)**: We extract 33 distinct 3D skeletal landmarks from the video feed.
2.  **Feature Normalization**: Landmarks are normalized to be invariant to camera distance and angle.
3.  **Classification (SVM)**: A trained Support Vector Machine (using Scikit-Learn) classifies the pose vectors.
4.  **Heuristic Correction**: Geometric rules (angles between joints) determines if your form matches the ideal biomechanics of the pose.

---

## 🚀 Deployment Guide

### 🔴 Backend (Hugging Face Spaces)

We use **Docker** on Hugging Face Spaces to serve the FastAPI backend.

1.  **Create Space**: Select **Docker** SDK on [Hugging Face Spaces](https://huggingface.co/spaces).
2.  **Structure**: Ensure `Dockerfile` is at the root.
3.  **Deploy**: The Space will build automatically.
4.  **URL**: Get your public API URL (e.g., `https://username-space.hf.space`).

> **Note**: The backend requires `libgl1` and specific `protobuf` versions to run headless MediaPipe on Linux. These are handled in our `Dockerfile`.

### 🔵 Frontend (Vercel)

The frontend is a Next.js application tailored for Vercel.

1.  **Import**: Connect your GitHub repo to Vercel.
2.  **Config**: Set Root Directory to `frontend`.
3.  **Env Var**: Add `NEXT_PUBLIC_API_URL` pointing to your Hugging Face backend.
4.  **Result**: Instant HTTPS deployment with global CDN.

---

## 💻 Local Development

Follow these steps to run YogaFlow AI on your machine.

### Prerequisites
- Node.js 20+
- Python 3.8+

### 1. Setup Backend

```bash
cd backend
pip install -r requirements.txt
python main.py
```
> Server running at `http://localhost:8000`

### 2. Setup Frontend

```bash
cd frontend
npm install
npm run dev
```
> App running at `http://localhost:3000`

*Don't forget to create a `.env.local` file in `frontend/` folder with `NEXT_PUBLIC_API_URL=http://localhost:8000`*

---

## 🔌 API Reference

The backend exposes a simple REST API.

**POST** `/classify`

Accepts a payload of 33 normalized landmarks and returns the predicted pose and corrections.

**Request Body:**
```json
{
  "landmarks": [
    { "x": 0.52, "y": 0.45, "z": -0.12, "visibility": 0.99 },
    ...
  ]
}
```

**Response:**
```json
{
  "pose_name": "Tree",
  "confidence": 0.99,
  "corrections": ["✅ posture perfect!"]
}
```

---

## 🛠️ Tech Stack

- **Frontend**: Next.js, React, TailwindCSS, Axios
- **Backend**: FastAPI, Uvicorn
- **AI/ML**: MediaPipe, Scikit-Learn, NumPy, OpenCV
- **DevOps**: Docker, Hugging Face, Vercel

---

## 👥 Authors

1. **Christine Kosasih**
2. **Vellyn Angeline**
3. **Gisella Jayata**