# guess a number randomly generated (through speech)

import google.cloud.texttospeech as tts
import os
import random

points = 10


# sets up the user, language of speech (both ways), and gender of google voice
client = tts.TextToSpeechClient.from_service_account_json("file for verifying your Google API - .json")
languageCode = 'input language code - e.g. fr-CA or en-US'
gender = tts.SsmlVoiceGender.NEUTRAL
voice = tts.VoiceSelectionParams(language_code = languageCode, ssml_gender = gender)

audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)

guess = -300

number = random.randint(-200, 200)
print(number)

while guess != number:

    guess = int(input())

    if number > guess:
        ourText = "too low"
        points -= 3

    if number < guess:
        ourText = "too high"
        points -= 3

    if number == guess:
        ourText = "You have" + str(points)

    synthesis_input = tts.SynthesisInput(text=ourText)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config)

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)

    os.startfile(r"file_path_for_the_audio")