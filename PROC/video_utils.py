# video_utils.py
import openai
import assemblyai
import os
from gtts import gTTS
from moviepy.editor import VideoFileClip
from api_keys import AZURE_OPENAI_API_KEY, ASSEMBLYAI_API_KEY

# Transcription using AssemblyAI
def transcribe_audio_assemblyai(audio_path):
    headers = {
        'authorization': ASSEMBLYAI_API_KEY,
        'content-type': 'application/json'
    }
    upload_url = 'https://api.assemblyai.com/v2/upload'

    # Upload the audio file to AssemblyAI
    with open(audio_path, 'rb') as audio_file:
        response = requests.post(upload_url, headers=headers, files={'file': audio_file})
        audio_url = response.json().get('upload_url')

    # Submit transcription job
    transcript_url = 'https://api.assemblyai.com/v2/transcript'
    response = requests.post(transcript_url, headers=headers, json={"audio_url": audio_url})
    transcript_id = response.json().get('id')

    # Wait for transcription to complete
    status_url = f'{transcript_url}/{transcript_id}'
    while True:
        result = requests.get(status_url, headers=headers).json()
        if result['status'] == 'completed':
            return result['text']
        elif result['status'] == 'failed':
            raise Exception('Transcription failed.')
    
    return None

# Correct transcription using GPT-4o
def correct_transcription_gpt(transcription_text):
    openai.api_key = AZURE_OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{
            "role": "user",
            "content": f"Please correct this transcription: {transcription_text}"
        }]
    )
    return response['choices'][0]['message']['content']

# Text-to-Speech using gTTS
def text_to_speech_gtts(text, output_path='output_audio.mp3'):
    tts = gTTS(text=text, lang='en')  # Convert the text to speech in English
    tts.save(output_path)             # Save the speech to a file
    print(f"Audio content written to {output_path}")
    return output_path

# Replace audio in video
def replace_audio_in_video(video_path, new_audio_path, output_video_path='final_video.mp4'):
    video = VideoFileClip(video_path)
    audio = mp.AudioFileClip(new_audio_path)
    new_video = video.set_audio(audio)
    new_video.write_videofile(output_video_path, codec='libx264', audio_codec='aac')
    return output_video_path

# Process the entire video
def process_video(video_path):
    video = VideoFileClip(video_path)
    audio_path = "extracted_audio.wav"
    video.audio.write_audiofile(audio_path)

    # Transcribe the audio using AssemblyAI
    transcription = transcribe_audio_assemblyai(audio_path)

    # Correct the transcription using GPT-4o
    corrected_transcription = correct_transcription_gpt(transcription)

    # Convert corrected text to speech using gTTS
    corrected_audio = text_to_speech_gtts(corrected_transcription)

    # Replace the original audio in the video
    output_video = replace_audio_in_video(video_path, corrected_audio)
    return output_video
