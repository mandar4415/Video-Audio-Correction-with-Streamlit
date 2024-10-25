# main.py
import streamlit as st
import os
from video_utils import process_video

st.title("Video Audio Replacement with AI-Generated Voice")

# Directory for storing videos
media_dir = 'C:\\Users\\Lenovo\\OneDrive\\Desktop\\int-sub\\Video-Audio-Correction-with-Streamlit\\PROC\\media\\'

# Ensure media directory exists
if not os.path.exists(media_dir):
    os.makedirs(media_dir)

# Define the path for a sample video
sample_video_path = os.path.join(media_dir, "video_sample.mp4")

# Video upload section
uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "mov", "avi"])

# Handling uploaded file
if uploaded_file is not None:
    # Save the uploaded video file in the media directory
    uploaded_video_path = os.path.join(media_dir, uploaded_file.name)
    with open(uploaded_video_path, 'wb') as f:
        f.write(uploaded_file.read())
    
    # Display the uploaded video
    st.video(uploaded_video_path)

    # Process the video if the 'Replace Audio' button is clicked
    if st.button("Replace Audio"):
        try:
            # Process the video to replace the audio
            corrected_audio_path = process_video(uploaded_video_path)
            
            # Check if audio was processed successfully
            if corrected_audio_path:
                st.audio(corrected_audio_path, format='audio/mp3')
                st.success("Audio replacement successful!")
            else:
                st.error("Failed to replace audio.")
        except Exception as e:
            st.error(f"Error during processing: {str(e)}")

# If no uploaded file, use sample video if available
else:
    if os.path.exists(sample_video_path):
        st.write("No file uploaded. Using sample video for demonstration.")
        st.video(sample_video_path)
        video_path = sample_video_path
        
        # Process sample video if the button is clicked
        if st.button("Replace Audio"):
            try:
                corrected_audio_path = process_video(sample_video_path)
                if corrected_audio_path:
                    st.audio(corrected_audio_path, format='audio/mp3')
                    st.success("Audio replacement successful!")
                else:
                    st.error("Failed to replace audio.")
            except Exception as e:
                st.error(f"Error during processing: {str(e)}")
    else:
        st.error("Please upload a video file or ensure the sample video exists in the 'media' folder.")
