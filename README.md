# Gesture_game
Mini AI project: Gesture controlled game using OpenCV and PyGame
#  Gesture Controlled Car Game

###  An AI-based car racing game controlled entirely through hand gestures!

This project combines **Computer Vision**, **Artificial Intelligence**, and **Game Development** to create a fun, interactive car game where you don’t need a keyboard or joystick — your **hand becomes the controller**!

---

##  Project Overview

The **Gesture Controlled Car Game** uses your webcam to track hand movements in real time.  
With the help of **MediaPipe** and **OpenCV**, the system detects the position of your hand and translates it into game controls for moving the car left, right, or stopping it.

As the game progresses, the difficulty level increases, making it both **challenging and exciting**.

---

##  Features

✅ Real-time hand gesture recognition  
✅ Contactless control using webcam  
✅ Increasing difficulty levels  
✅ Dynamic obstacles and scoring system  
✅ Smooth car motion and road animation  

---

##  Technologies Used

| Technology | Purpose |
| **Python** | Main programming language |
| **OpenCV** | Captures webcam input |
| **MediaPipe** | Detects and tracks hand gestures |
| **Pygame** | Builds the game interface and handles motion logic |

---

##  How It Works

1. The **webcam** captures live video of your hand.  
2. **MediaPipe** processes the frame and detects hand landmarks.  
3. The **x-position** of your index finger is used to move the car horizontally.  
4. The player avoids **obstacles** that appear randomly.  
5. The **score** increases with time, and **levels** rise as the game speeds up.

---

##  Controls

| Hand Gesture | Action |
| ✋ Palm | Stop the car |
| 👉 Move hand right | Move car right |
| 👈 Move hand left | Move car left |

*(Move your hand in front of the webcam horizontally to control the car.)*

---

##  Output Preview

| Scene | Description |
| ![Start Screen](assets/output_start.png) | Game Start Screen |
| ![Gameplay](assets/output_play.png) | Car Moving using Gestures |
| ![Game Over](assets/output_crash.png) | Collision/Game Over |

---

##  Installation & Setup

###  Clone the repository:
```bash
git clone https://github.com/yourusername/gesture-car-game.git
cd gesture-car-game
