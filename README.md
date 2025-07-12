# 🧠 Multi-Modal Desktop Assistant (Gesture + Voice + Chat)

This project is a powerful **AI-powered desktop assistant** that integrates **gesture control**, **voice commands**, and a **Gemini chatbot GUI** to enable hands-free and intelligent interaction with your computer.

---

## ✨ Features

- ✅ **Gesture Controls** using OpenCV and MediaPipe:
  - Control **volume** and **brightness** with hand gestures.
  - **Mouse control**, **clicks**, **minimize/maximize**, **alt-tab**, **close window**, and **media controls** (play/pause, next/previous).
  
- 🎙️ **Voice Assistant** (like "Hey Jarvis"):
  - Open/create text files and perform read/write operations.
  - Open or close applications like YouTube, Chrome, and Calculator.
  - Replace words inside open files via voice.

- 🤖 **Gemini AI Chat Interface**:
  - Chat with Gemini AI in a Tkinter-based GUI.
  - Get answers, write code, or assist with tasks using natural language.

---

## 📂 Project Structure

```bash
.
├── main.py           # Main Python file with GUI, voice assistant, gesture control
├── requirements.txt  # Required packages
└── README.md         # This file
⚙️ Requirements
Install Python libraries via pip:

pip install opencv-python mediapipe pyautogui pycaw comtypes numpy wmi keyboard speechrecognition google-generativeai

Also ensure:
1)You have Python 3.10+
2)A working webcam and microphone
3)Google Chrome is installed (for voice assistant app control)

🔐 Gemini API Key
Replace this line in your code with your own Gemini key:

genai.configure(api_key="YOUR_API_KEY")
Get it from: https://ai.google.dev/

▶️ How to Run
Clone or download this repo.
Run the script:

python main.py

The program will:

Start the gesture control using your webcam.

Launch the Gemini chatbot GUI.

Begin listening for voice commands in the background.

🖐 Gesture Actions Guide
Gesture	Action

Left hand controls
All fingers up (hand open)		         | Adjust brightness up/down by moving hand up/down     
Thumb + Index finger tips close touch  | (left hand)	Perform left click                      
Thumb + Ring finger tips close touch	 | (thumb-ring touch)	Perform double click              
Thumb + Middle finger tips touch	     | Previous track in media playback                     

Right hand  controls
All fingers up (open palm)		             | Adjust volume by moving hand up/down
Index + Middle fingers up (others down)		 | Control mouse cursor
Thumb + Pinky finger tips touch		         | Play/Pause media
Thumb + Middle finger tips toucgh	         | Next track
Thumb + Index finger tips touch		         | Right click
All fingers down (rock gesture)		         | Minimize window
Thumb + Tip of ring finger (little finger) | Trigger Alt+Tab for window switch

Both hand together controls
Both hand Index finger touch                                                                                 | Maximize current window
Left hand index finger touch right hand index finger +Left hand middle finger touch right hand middle finegr | Close current window

🗣 Voice Commands (Examples)
"Hey Jarvis open new file"

"Hey Jarvis open existing file"

"Hey Jarvis close file"

"Hey Jarvis open YouTube"

"Hey Jarvis close Chrome"

"Hey Jarvis replace" (replace words in open file)

You will be prompted for file names or words when needed.

💡 Gemini Chat GUI
Type queries and press Enter or click ➤.

Responses will appear from Gemini AI using your configured API key.

📌 Notes
Tested on Windows with Python 3.10.

Admin privileges may be needed for brightness control.

Voice recognition uses Google's free Speech Recognition API.

