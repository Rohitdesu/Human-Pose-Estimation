# Human Pose Estimation with OpenCV and TensorFlow

This project implements human pose estimation using OpenCV and TensorFlow's pre-trained models. It allows users to upload images and visualize key body parts and their connections, demonstrating real-time human pose detection.

## Features
- Detects human poses in images using a pre-trained TensorFlow model (`graph_opt.pb`).
- Identifies key body parts, including the nose, shoulders, elbows, wrists, hips, knees, and ankles.
- Visualizes the pose using OpenCV by drawing lines and ellipses on detected body parts.
- Provides a Streamlit-based web app for easy image uploads and visualization.

## Requirements

To run the project, ensure you have the following dependencies installed:

- Python 3.x
- OpenCV
- TensorFlow
- Streamlit
- PIL (Python Imaging Library)
- NumPy

### Installing Dependencies

You can install the required libraries using pip:

``bash
pip install opencv-python tensorflow streamlit pillow numpy

## Project Structure
 - pose_estimation.py: Main Python script for pose detection. It contains the logic for loading the model, processing images, and visualizing key points and poses.
 - stand.jpg: Demo image 
 - graph_opt.pb: The TensorFlow model used for human pose detection.

## How to Use
 - Streamlit Web Application
 - Clone or download the repository to your local machine.
 - Navigate to the project directory in your terminal.
 -  Run the following command to start the Streamlit app:
streamlit run pose_estimation.py streamlit
The app will open in your browser, where you can upload an image to detect poses. You can adjust the threshold for detecting key points using the slider.

Pose Estimation Explanation
The model uses a TensorFlow-based pre-trained neural network to detect human poses by identifying the locations of 18 body parts, including the head, limbs, and torso. The key parts detected are:

 - Nose
 - Neck
 - Shoulders
 - Elbows
 - Wrists
 - Hips
 - Knees
 - Ankles
 - Eyes
 - Ears
The detected parts are connected by lines to form a skeleton representing the pose.


## Acknowledgments
OpenCV for the dnn module and pre-trained models.
TensorFlow for deep learning capabilities.
Streamlit for building the interactive web app.
PIL for image processing.

