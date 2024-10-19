# video_utils.py
import openai
import assemblyai
import pyttsx3
from TTS.api import TTS
from moviepy.editor import VideoFileClip
from api_keys import AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT, ASSEMBLYAI_API_KEY

# Transcription using AssemblyAI
def transcribe_audio_assemblyai(audio_path):
    headers = {
        'authorization': ASSEMBLYAI_API_KEY,
        'content-type': 'application/json'
    }
    url = "https://api.assemblyai.com/v2/transcript"
    
    with open(audio_path, 'rb') as f:
        data = f.read()

    # Send to AssemblyAI
    response = requests.post(url, headers=headers, files={"audio": data})
    return response.json().get('text')

# Use Whisper to transcribe audio
def transcribe_audio_whisper(audio_path):
    model = openai.Whisper("whisper-1")
    with open(audio_path, "rb") as f:
        transcription = model.transcribe(f)
    return transcription['text']

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

# Text-to-Speech using Coqui TTS
def text_to_speech_coqui(corrected_text, output_path='output_audio.wav'):
    tts = TTS("tts_models/en/ljspeech/tacotron2-DDC")
    tts.tts_to_file(text=corrected_text, file_path=output_path)
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

    # Transcribe the audio
    transcription = transcribe_audio_assemblyai(audio_path)
    
    # Correct the transcription
    corrected_transcription = correct_transcription_gpt(transcription)
    
    # Convert corrected text to speech
    corrected_audio = text_to_speech_coqui(corrected_transcription)
    
    # Replace the original audio
    output_video = replace_audio_in_video(video_path, corrected_audio)
    return output_video
