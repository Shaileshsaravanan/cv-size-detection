# 🎉 cv-size-detection

Welcome to the **cv-size-detection** GitHub repository! 🚀 This project is all about turning your webcam into a measuring machine using the magic of computer vision. With the help of OpenCV and Aruco markers, you can now detect objects and measure their dimensions right from your camera feed in real-time. It's like having a digital ruler, but way cooler! 😎

## Table of Contents

- [What’s This About?](#whats-this-about)
- [Get Set Up](#get-set-up)
- [How to Play](#how-to-play)
- [Repo Rundown](#repo-rundown)

## What’s This About? 🧐

Imagine being able to measure objects just by pointing your webcam at them. That's exactly what this project does! By placing an Aruco marker (think of it like a special QR code) in the camera’s view, our script can detect objects and tell you their exact size in centimeters. All of this happens in real-time, so you can wave your objects around and watch the measurements update on the fly!

## Get Set Up 🛠️

### Prerequisites

To get started, you'll need:
- Python 3.x
- OpenCV
- NumPy 

### Install the Goodies

1. First, clone this repo:
    ```bash
    git clone https://github.com/shaileshsaravanan/cv-size-detection.git
    cd cv-size-detection
    ```

2. Then, install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## How to Play 🎮

### Fire Up the Object Size Detector

Once you're all set up, it’s time to launch the magic:

```bash
python main/measure_object_size_camera.py
```

**Note:** Make sure your webcam is plugged in and ready to go. By default, the script looks for it on input "1" (`cv2.VideoCapture(1)`), but if it's your primary camera, just switch it to "0" (`cv2.VideoCapture(0)`).

### Watch the Magic Happen ✨

- As the script runs, you'll see your webcam feed, and anything the script detects will get a cool blue rectangle around it. 
- The dimensions of the object (in centimeters) will pop up next to it like a video game HUD! 
- Remember, the Aruco marker is the star here—it needs to be in the frame for the measurements to work their magic. 

## Repo Rundown 🗂️

Here’s a quick tour of what you’ll find in this repository:

- **main/**: The brain of the operation.
  - `object_detector.py`: This script handles all the object-detecting magic.
  - `measure_object_size_camera.py`: The main show! It captures the video, detects the objects, and tells you their size. It’s like a high-tech measuring tape.
  
- **train + test/**: training and testing done to achieve current iteration!