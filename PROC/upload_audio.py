import requests

# Define the function to upload audio to AssemblyAI
def upload_audio_to_assemblyai(audio_path, api_key):
    headers = {
        'authorization': api_key,
    }
    upload_url = 'https://api.assemblyai.com/v2/upload'

    # Open the audio file in binary mode
    with open(audio_path, 'rb') as audio_file:
        # Send POST request to upload the file
        response = requests.post(upload_url, headers=headers, files={'file': audio_file})
        
    # Check if the upload was successful
    if response.status_code == 200:
        audio_url = response.json().get('upload_url')
        print(f"Audio successfully uploaded. URL: {audio_url}")
        return audio_url
    else:
        print(f"Failed to upload audio. Status code: {response.status_code}")
        print(response.json())
        return None

# Example usage
api_key = "9921a273a9e44afb93ad2f9a8c7a0038"     
audio_path = "C:\\Users\\Lenovo\\OneDrive\\Desktop\\int-sub\\Video-Audio-Correction-with-Streamlit\\PROC\\media\\audio_sample.wav" 
# Call the function and get the upload URL
audio_url = upload_audio_to_assemblyai(audio_path, api_key)
