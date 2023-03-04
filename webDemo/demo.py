from flask import Flask, render_template, request
from werkzeug.utils import secure_filename
from datetime import timedelta
import os

# import the Google Cloud client library
from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['ALLOWED_EXTENSIONS'] = {'wav', 'mp3'}

# import the transcribe_audio function from before

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


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'audio_file' not in request.files:
            return render_template('index.html', error='No file part')
        file = request.files['audio_file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return render_template('index.html', error='No selected file')
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            # call the transcribe_audio function to transcribe the audio
            transcribed_text = transcribe_audio(file_path)
            # convert the transcribed text to movie subtitle text format
            subtitle_text = ''
            subtitle_num = 1
            for line in transcribed_text.split('\n'):
                if line.strip() != '':
                    subtitle_text += f'{subtitle_num}\n'
                    start_time = timedelta(seconds=line.words[0].start_time.seconds)
                    end_time = timedelta(seconds=line.words[-1].end_time.seconds)
                    subtitle_text += f'{start_time} --> {end_time}\n'
                    subtitle_text += f'{line}\n\n'
                    subtitle_num += 1
            return render_template('index.html', subtitle_text=subtitle_text)
        else:
            return render_template('index.html', error='Invalid file type')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
