import streamlit as st
from PIL import Image
import numpy as np
import cv2
import os

# Paths and configurations
DEMO_IMAGE = 'stand.jpg'
BODY_PARTS = { "Nose": 0, "Neck": 1, "RShoulder": 2, "RElbow": 3, "RWrist": 4,
               "LShoulder": 5, "LElbow": 6, "LWrist": 7, "RHip": 8, "RKnee": 9,
               "RAnkle": 10, "LHip": 11, "LKnee": 12, "LAnkle": 13, "REye": 14,
               "LEye": 15, "REar": 16, "LEar": 17, "Background": 18 }

POSE_PAIRS = [ ["Neck", "RShoulder"], ["Neck", "LShoulder"], ["RShoulder", "RElbow"],
               ["RElbow", "RWrist"], ["LShoulder", "LElbow"], ["LElbow", "LWrist"],
               ["Neck", "RHip"], ["RHip", "RKnee"], ["RKnee", "RAnkle"], ["Neck", "LHip"],
               ["LHip", "LKnee"], ["LKnee", "LAnkle"], ["Neck", "Nose"], ["Nose", "REye"],
               ["REye", "REar"], ["Nose", "LEye"], ["LEye", "LEar"] ]

width = 368
height = 368
inWidth = width
inHeight = height

# Ensure the model file exists
if not os.path.exists("graph_opt.pb"):
    raise FileNotFoundError("The file 'graph_opt.pb' was not found. Please provide the correct path.")

# Load the pre-trained model
net = cv2.dnn.readNetFromTensorflow("graph_opt.pb")

# Pose detection function
def poseDetector(frame, threshold=0.2):
    frameWidth = frame.shape[1]
    frameHeight = frame.shape[0]
    net.setInput(cv2.dnn.blobFromImage(frame, 1.0, (inWidth, inHeight), (127.5, 127.5, 127.5), swapRB=True, crop=False))
    out = net.forward()
    out = out[:, :19, :, :]

    assert len(BODY_PARTS) == out.shape[1]
    points = []
    for i in range(len(BODY_PARTS)):
        heatMap = out[0, i, :, :]
        _, conf, _, point = cv2.minMaxLoc(heatMap)
        x = (frameWidth * point[0]) / out.shape[3]
        y = (frameHeight * point[1]) / out.shape[2]
        points.append((int(x), int(y)) if conf > threshold else None)
    
    for pair in POSE_PAIRS:
        partFrom, partTo = pair
        idFrom, idTo = BODY_PARTS[partFrom], BODY_PARTS[partTo]
        if points[idFrom] and points[idTo]:
            cv2.line(frame, points[idFrom], points[idTo], (0, 255, 0), 3)
            cv2.ellipse(frame, points[idFrom], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)
            cv2.ellipse(frame, points[idTo], (3, 3), 0, 0, 360, (0, 0, 255), cv2.FILLED)

    return frame

# Streamlit App
def run_streamlit_app():
    st.title("Human Pose Estimation with OpenCV")
    st.text("Upload an image with clearly visible body parts for pose estimation.")
    
    img_file_buffer = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    threshold = st.slider('Threshold for detecting key points', min_value=0, value=20, max_value=100, step=5) / 100
    
    if img_file_buffer is not None:
        image = np.array(Image.open(img_file_buffer))
    else:
        st.warning("Using default demo image.")
        image = np.array(Image.open(DEMO_IMAGE))
    
    st.subheader("Original Image")
    st.image(image, caption="Uploaded Image", use_column_width=True)

    output = poseDetector(image, threshold)
    st.subheader("Pose Estimated Image")
    st.image(output, caption="Pose Estimated", use_column_width=True)

# Standalone Script
def run_standalone():
    input_image = cv2.imread(DEMO_IMAGE)
    output_image = poseDetector(input_image, threshold=0.2)
    cv2.imwrite("Output-Image.png", output_image)
    print("Pose estimation completed and saved as 'Output-Image.png'.")

# Main Functionality
if __name__ == "__main__":
    import sys
    # If Streamlit app
    if "streamlit" in sys.argv:
        run_streamlit_app()
    else:
        run_standalone()
