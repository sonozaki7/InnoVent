import io
import os

# import the Google Cloud client library
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums


  
transcribe_audio('audio_file.wav', speaker_name='John')