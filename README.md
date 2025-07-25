# 🔦 Hand Gesture Controlled LED Brightness with Arduino & Mediapipe
This project allows you to control the brightness of three individual LEDs connected to an Arduino using hand gestures detected via webcam using MediaPipe and OpenCV in Python.


## 🛠️ Features
- Control LED brightness with hand pinching gestures
- Visual selection of LEDs via on-screen colored boxes
- Real-time hand tracking using MediaPipe
- Smooth serial communication between Python and Arduino
- Interactive UI with OpenCV overlays


## 🖥️ How It Works
- A webcam captures your hand gestures.
- When you pinch your thumb and index finger, it selects an LED box (red, yellow, or blue).
- The distance between your fingers controls the brightness (closer = dimmer, farther = brighter).
- The Python script sends brightness values over serial to Arduino in the format pin:value.


## ⚡ Steps to run this
- Upload the code to Arduino Board.
- Change the COM Port in the code as of Arduino.
- Run the Python code.
- Enjoy🎉.



## 🧰 Hardware Required
- Arduino Uno/Nano (or compatible board)
- 3 x LEDs
- 3 x 220Ω resistors
- Jumper wires
- Breadboard
- USB cable for Arduino


## 🔌 Arduino Wiring
- LED	Arduino Pin
- Red (LED-1)	D9
- Yellow (LED-2)	D10
- Blue (LED-3)	D11
- Each LED should be connected via a resistor (~220Ω) to GND.
