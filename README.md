# VidSnapAI

A fully automated reel/video generator that converts text into audio and merges it with video templates using FFmpeg.  
Deployed on **Render** using Docker.

## 🚀 Live Demo  
👉 https://web-production-3653.up.railway.app/

## ✨ Features
- Text-to-Speech using **gTTS**
- Video generation using **FFmpeg**
- Flask backend
- Dockerized deployment
- Works on Render free tier

## 📂 Project Structure
```
├── main.py
├── generate_process.py
├── text_to_audio.py
├── requirements.txt
├── Dockerfile
├── static/
├── templates/
└── user_uploads/
```

## 🛠 Tech Stack
- Python 3.10
- Flask
- gTTS
- FFmpeg
- Docker
- Render (Hosting)

## 🧪 Running Locally

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Start the Flask server
```bash
python main.py
```

### 3. Open in browser
```
http://localhost:10000
```

## 🚀 Deploying to Render

1. Push code to GitHub  
2. Add `Dockerfile` and `render.yaml`  
3. Create new Render Web Service  
4. Deploy 🎉

## 📝 License
MIT License
