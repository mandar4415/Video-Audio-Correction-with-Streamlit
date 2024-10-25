# main.py
import streamlit as st
import os
from video_utils import process_video

st.title("Video Audio Replacement with AI-Generated Voice")

# Check if a sample video exists in the media folder for testing
sample_video_path = "media/video_sample.mp4"
use_sample = False

# Video upload section
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

# If an uploaded video file is provided, use it
if uploaded_file is not None:
    with open('temp_video.mp4', 'wb') as f:
        f.write(uploaded_file.read())
    video_path = 'temp_video.mp4'
    st.video(video_path)
else:
    # Otherwise, use the sample video if it exists
    if os.path.exists(sample_video_path):
        st.write("No file uploaded. Using sample video for demonstration.")
        video_path = sample_video_path
        use_sample = True
        st.video(video_path)
    else:
        st.error("Please upload a video file or ensure the sample video exists in the 'media' folder.")

# Start the process when the button is clicked
if st.button("Replace Audio"):
    if video_path:
        corrected_audio_path = process_video(video_path)
        st.audio(corrected_audio_path, format='audio/mp3')
    else:
        st.error("No video available for processing.")
