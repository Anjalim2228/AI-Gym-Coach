# 🏋️ AI Gym Coach

<div align="center">

### 🤖 AI-Powered Personal Fitness Trainer

**Track • Analyze • Correct • Improve**

*A real-time AI fitness coach that monitors your exercise posture, counts repetitions, and provides intelligent feedback using Computer Vision and Artificial Intelligence.*

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge\&logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-Web_App-red?style=for-the-badge\&logo=streamlit)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer_Vision-green?style=for-the-badge\&logo=opencv)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Pose_Detection-orange?style=for-the-badge)
![AI](https://img.shields.io/badge/AI-Powered-purple?style=for-the-badge)

</div>

---

# 📖 Overview

AI Gym Coach is an AI-powered fitness assistant that helps users perform exercises with the correct posture using real-time computer vision.

The application uses a webcam to detect body landmarks, analyze exercise movements, count repetitions, and provide intelligent feedback. It aims to bring the experience of a personal gym trainer directly to the user's device without requiring specialized hardware.

This project combines Artificial Intelligence, Computer Vision, and an interactive Streamlit interface to make fitness training smarter, more engaging, and accessible.

---

# ✨ Features

* 🎥 Real-time webcam exercise tracking
* 🤖 AI-powered posture analysis
* 🧍 Human pose detection using MediaPipe
* 🔢 Automatic repetition counting
* ✅ Correct and incorrect posture detection
* 💬 Intelligent workout feedback
* 🔊 Voice responses using Google Text-to-Speech
* 📊 Workout monitoring dashboard
* ⚡ Fast and lightweight Streamlit interface

---

# 🛠️ Tech Stack

| Category        | Technology |
| --------------- | ---------- |
| Language        | Python     |
| Frontend        | Streamlit  |
| Computer Vision | OpenCV     |
| Pose Detection  | MediaPipe  |
| AI Integration  | Groq API   |
| Data Processing | Pandas     |
| Text-to-Speech  | gTTS       |

---

# 📂 Project Structure

```text
AI_Gym_Coach/
│
├── Main App/
│   ├── app.py
│   ├── requirements.txt
│   ├── assets/
│   ├── utils/
│   └── ...
│
├── Landing Page/
│
├── README.md
│
└── .gitignore
```

---

# 🚀 Installation

### Clone Repository

```bash
git clone https://github.com/your-username/AI-Gym-Coach.git
```

### Move into the project

```bash
cd AI-Gym-Coach
```

### Install Dependencies

```bash
pip install -r "Main App/requirements.txt"
```

### Run the Application

```bash
streamlit run app.py
```

---

# ⚙️ Requirements

* Python 3.10+
* Webcam
* Internet connection (if AI API is used)

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create a `.env` file if required.

```env
GROQ_API_KEY=your_api_key_here
```

---

# 🧠 How It Works

1. The user launches the Streamlit application.
2. The webcam captures live video.
3. MediaPipe detects body landmarks in real time.
4. Exercise angles and posture are calculated.
5. The system counts repetitions automatically.
6. Incorrect posture is identified and corrected through AI feedback.
7. Voice assistance guides the user during workouts.
8. Progress is displayed through the dashboard.

---

# 🤖 AI Pipeline

```
User
   │
   ▼
Webcam
   │
   ▼
OpenCV
   │
   ▼
MediaPipe Pose Detection
   │
   ▼
Pose Analysis
   │
   ▼
Rep Counter
   │
   ▼
AI Feedback
   │
   ▼
Voice Response (gTTS)
   │
   ▼
Streamlit Dashboard
```

---

# 🎯 Applications

* Personal Fitness Coach
* Home Workout Assistant
* Gym Companion
* Exercise Form Correction
* Fitness Education
* Physical Rehabilitation Support

---

# 📈 Future Enhancements

* Multiple exercise support
* Personalized workout plans
* Workout history
* User authentication
* Progress analytics
* Calorie estimation
* BMI tracking
* Diet recommendations
* Cloud database integration
* Mobile application
* Wearable device support

---

# 📚 Learning Outcomes

This project helped in gaining practical experience with:

* Artificial Intelligence
* Computer Vision
* Human Pose Estimation
* Real-Time Video Processing
* Python Development
* Streamlit Web Applications
* API Integration
* AI-assisted User Interaction

---

# 🤝 Contributing

Contributions are welcome!

1. Fork the repository
2. Create a new feature branch
3. Commit your changes
4. Push the branch
5. Open a Pull Request

---

# 📄 License

This project is developed for educational and learning purposes.

---

# 👩‍💻 Author

**Anjali Mane**

* GitHub: [https://github.com/your-username](https://github.com/Anjalim2228)
* LinkedIn: [https://linkedin.com/in/your-profile](https://www.linkedin.com/in/anjali-mane-7161ab2bb/)

---

<div align="center">

⭐ If you found this project useful, consider giving it a **Star** on GitHub!

</div>
