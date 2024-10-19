# main.py
import streamlit as st
import moviepy.editor as mp
from video_utils import process_video
import api_keys

st.title("Video Audio Replacement with AI-Generated Voice")

# Video upload section
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

if uploaded_file is not None:
    with open('temp_video.mp4', 'wb') as f:
        f.write(uploaded_file.read())
    st.video(uploaded_file)
    
    # Start the process when the button is clicked
    if st.button("Replace Audio"):
        corrected_audio_path = process_video('temp_video.mp4')
        st.audio(corrected_audio_path, format='audio/mp3')
