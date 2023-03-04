import io
import os

# import the Google Cloud client library
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

def transcribe_audio(audio_file, speaker_name=None):
    """
    Transcribes an audio file using the Google Cloud Speech-to-Text API
    and displays the transcribed text on the screen along with the name of the speaker (if provided).
    
    Parameters:
    audio_file (str): The path to the audio file to transcribe.
    speaker_name (str): The name of the speaker (optional).
    
    Returns:
    str: The transcribed text.
    """
    
    # set up the Google Cloud client
    client = speech_v1.SpeechClient()

    # open the audio file and read the contents into memory
    with io.open(audio_file, 'rb') as audio_file_obj:
        content = audio_file_obj.read()

    # set up the speech recognition request
    audio = speech_v1.types.RecognitionAudio(content=content)
    config = speech_v1.types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code='en-US',
        enable_word_time_offsets=True,
        diarization_config=speech_v1.types.SpeakerDiarizationConfig(
            enable_speaker_diarization=True,
            min_speaker_count=2,
            max_speaker_count=2
        )
    )

    # send the request to the Google Cloud Speech-to-Text API
    response = client.recognize(config, audio)

    # parse the response and extract the transcribed text
    results = response.results
    transcribed_text = ''
    for result in results:
        alternatives = result.alternatives
        for alternative in alternatives:
            transcribed_text += alternative.transcript

    # display the transcribed text on the screen, along with the speaker name (if provided)
    if speaker_name is not None:
        print(f"{speaker_name}: {transcribed_text}")
    else:
        print(transcribed_text)
    
    # return the transcribed text
    return transcribed_text

  
  transcribe_audio('audio_file.wav', speaker_name='John')
