# 1) import all the libraries
from google.cloud import speech_v1
from google.cloud.speech_v1 import types
import soundfile as sf
import sounddevice as sd
from scipy.io.wavfile import write
import io
import google.cloud.texttospeech as tts
import os

# 2) Authenticate and create a client
j_path = 'file for verifying your Google API - .json'
client = speech_v1.SpeechClient.from_service_account_json(j_path)

# 3) Define Samples and Duration of voice recording
sampleRate = 44100

recDuration = 5
totalSamples = int(sampleRate * recDuration)

# 4) Record voice
print('Start Recording')
myRecording = sd.rec(totalSamples, sampleRate, 1)
sd.wait()
print('Done Recording')

# 5) Write as WAV file, then convert to FLAC
write('voiceRecording.wav', sampleRate, myRecording)

data, recSampleRate = sf.read('voiceRecording.wav')
sf.write('voiceRecording.FLAC', data, sampleRate)

# 6) Define Config
encoding = speech_v1.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
languageCode = 'en-US'
config = {'encoding':encoding, 'sample_rate_hertz':sampleRate, 'language_code':languageCode}

# 7) Grab the FLAC file and send it to Google
path = 'voiceRecording.FLAC'
with io.open(path, 'rb') as audio_file:
    content = audio_file.read()
    audio = types.RecognitionAudio(content=content)
    response = client.recognize({"config": config, "audio": audio})

# 8) Output response from Google
print(response)

for result in response.results:
    print(result.alternatives[0].transcript)

cli = tts.TextToSpeechClient.from_service_account_json("file for verifying your Google API - .json")
languageCode = 'en-US' # can be changed to an language code available for Google APIs
gender = tts.SsmlVoiceGender.NEUTRAL
voice = tts.VoiceSelectionParams(language_code = languageCode, ssml_gender = gender)

ac = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)

synthesis_input = tts.SynthesisInput(text="Hello, how are you?")

if result.alternatives[0].transcript == "hello":
    rep = cli.synthesize_speech(input=synthesis_input, voice=voice, audio_config=ac)

    with open("output.mp3", "wb") as out:
        out.write(rep.audio_content)

    os.startfile(r"path for output.mp3")