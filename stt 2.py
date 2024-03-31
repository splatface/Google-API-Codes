# some of the code in this program is explained in other programs in this folder

from google.cloud import speech_v1
from google.cloud.speech_v1 import types
import soundfile as sf
import sounddevice as sd
from scipy.io.wavfile import write
import io
import google.cloud.texttospeech as tts
import os
import time
import random
import re
import datetime as dt
import python_weather
import asyncio

client = tts.TextToSpeechClient.from_service_account_json("file for verifying your Google Cloud API - .json")
cli = speech_v1.SpeechClient.from_service_account_json("file for verifying your Google Cloud API - .json")

x = 0
ourText = ""



def s_to_audio(ourText):
    synthesis_input = tts.SynthesisInput(text = ourText)

    languageCode = 'en-US'
    gender = tts.SsmlVoiceGender.NEUTRAL
    voice = tts.VoiceSelectionParams(language_code = languageCode, ssml_gender = gender)

    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.MP3)

    response = client.synthesize_speech(input=synthesis_input, voice=voice, audio_config=audio_config) # audio_config = to the variable above, not other way around

    with open("output.mp3", "wb") as out:
        out.write(response.audio_content)
    
    os.startfile(r"path for output.mp3")
    time.sleep(3)



def record():
    sampleRate = 44100

    recDuration = 3
    totalSamples = int(sampleRate * recDuration)

    print("Start Recording")
    myRecording = sd.rec(totalSamples, sampleRate, 1)
    sd.wait()
    print("Done Recording")

    write('voiceRecording.wav', sampleRate, myRecording)

    data, recSampleRate = sf.read('voiceRecording.wav')
    sf.write('voiceRecording.FLAC', data, sampleRate)

    encoding = speech_v1.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
    languageCode = 'en-US'
    config = {'encoding':encoding, 'sample_rate_hertz':sampleRate, 'language_code':languageCode}

    path = 'voiceRecording.FLAC'
    with io.open(path, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
        rep = cli.recognize({"config": config, "audio": audio})

    for result in rep.results:
        speech = result.alternatives[0].transcript
        print(result.alternatives[0].transcript)
        return speech
    return ""



def has_numbers(input):
    includes =  any(string.isdigit() for string in input)
    
    if includes == True:
        finale = re.findall(r'\d+', input)
        return finale

    else:
        no_understand()
        return [0]



def question():
    
    if x == 0:
        s_to_audio("How can I help you?")

    sampleRate = 44100

    recDuration = 4
    totalSamples = int(sampleRate * recDuration)

    print("Start Recording")
    myRecording = sd.rec(totalSamples, sampleRate, 1)
    sd.wait()
    print("Done Recording")

    write('voiceRecording.wav', sampleRate, myRecording)

    data, recSampleRate = sf.read('voiceRecording.wav')
    sf.write('voiceRecording.FLAC', data, sampleRate)

    encoding = speech_v1.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
    languageCode = 'en-US'
    config = {'encoding':encoding, 'sample_rate_hertz':sampleRate, 'language_code':languageCode}

    path = 'voiceRecording.FLAC'
    with io.open(path, 'rb') as audio_file:
        content = audio_file.read()
        audio = types.RecognitionAudio(content=content)
        rep = cli.recognize({"config": config, "audio": audio})

    for result in rep.results:
        speech = result.alternatives[0].transcript
        print(result.alternatives[0].transcript)
        return speech
    
    return ""
   


def no_understand():
    s_to_audio("I'm not sure I understand. Can you repeat that?")



def coin_flip():
    flip = random.randint(0,1)
    bet = record()

    if "no" in bet:
        if flip == 0:
            ourText = "heads"
        else:
            ourText = "tails"

        s_to_audio(ourText)
    
    if "yes" in bet:
        s_to_audio("Heads or tails?")
        coin = record()

        if flip == 0 and "heads" in coin:
            ourText = "win"
        if flip == 0 and "tails" in coin:
            ourText = "lose"
        if flip == 1 and "tails" in coin:
            ourText = "win"
        if flip == 1 and "heads" in coin:
            ourText = "lose"
        
        s_to_audio(ourText)



def roll_a_dice():
    s_to_audio("How would you rate this dice on a scale from one to ten?")
    load = record()



    if "one" in load or "two" in load or "none" in load or "how would I know" in load or "I haven't used it yet" in load or "zero" in load or "four" in load or "negative" in load:
        roll = random.randint(1,6)

        if roll == 1:
            ourText = "one"
        
        if roll == 2:
            ourText = "two"
            
        if roll == 3:
            ourText = "three"
        
        if roll == 4:
            ourText = "four"
        
        if roll == 5:
            ourText = "five"
        
        if roll == 6:
            ourText = "six"
        
        s_to_audio(ourText)
    

    # random conditions and results under different types of loaded dice
    if "nine" in load or "eight" in load or "the best" in load or "six" in load: #so other people don't know you are loading the dice 
        s_to_audio("Lucky number?")
        chosen_num = record()

        numb = has_numbers(chosen_num)
        answer = int(numb[0])

        if answer % 7 == 0 and answer % 2 != 0 and answer % 10 != 0 and answer % 222 != 0: #only divisible by 7, not 10 or 2 or 222
            ourText = "one"
        elif answer % 2 == 0 and answer % 7 != 0 and answer % 10 != 0 and answer % 222 != 0: #only divisible by 2, not 7 or 10 or 222
            ourText = "two"
        elif answer % 2 == 0 and answer % 7 == 0 and answer % 10 != 0 and answer % 222 != 0: #divisible by 2 and 7, not 10 or 222
            ourText = "three"
        elif answer**2 % 10 == 0 and answer % 7 != 0 and answer % 222 != 0: #divisible by 2 and 10, but not 7 or 222
            ourText = "four"
        elif (answer**3 + 2) % 2 == 0 and answer % 7 != 0 and answer % 6 == 0 and answer % 222 != 0: #divisible by 2 and 6, not 7 or 222
            ourText = "five"
        elif answer % 2 == 0 and answer % 7 == 0 and answer % 10 == 0 and answer % 222 != 0: #divisible by 2, 7, and 10, not by 222
            ourText = "six"
        elif answer % 222 == 0: #divisible by 222???
            ourText = "seven?"
            print("!!!")
        else: #none
            ourText = "two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two"
            print("two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two two \n ")
        
        s_to_audio(ourText)
        print("Finished!")
        time.sleep(7)



    if "three" in load or "five" in load or "seven" in load or "ten" in load:
        s_to_audio("Refused. Next time please pick a non-default option. Have a nice day. (and better luck next time)")



    if "no" in load:
        s_to_audio("How many sides?")
        sides_str = record()
        if "negative" in sides_str:
            return "Valid number please"
        
        else:
            blank = has_numbers(sides_str)
            sides_int = int(blank[0])

            number = random.randint(0, sides_int)
            ourText = str(number)

            s_to_audio(ourText)


    #0, 1, 2, 4, none, negative in normal dice
    #6, 8, 9, best in loaded dice
    #3, 5, 7, 10 in refusal to roll dice
    #refusal to rate = change number of sides from 6 to infinity


def calculator():

    #1st number
    print("What is the first number?")
    a = record()

    f_num_contains = has_numbers(a)
    print(f_num_contains)
    a = int(f_num_contains[0])

    #2nd number
    print("What is the second number?")
    b = record()

    s_num_contains = has_numbers(b)
    print(s_num_contains)
    b = int(s_num_contains[0])

    #operation
    print("What is the operation?")

    operation = record()

    if "multiplication" in operation:
        c = a*b
    elif "division" in operation:
        c = a/b
    elif "addition" in operation:
        c = a+b
    elif "subtraction" in operation:
        c = a-b
    else:
        no_understand()
    
    s_to_audio(str(c))
    
    correct = record()

    if "no" in correct:
        print("1st number:")
        one = int(input())

        print("2nd number:")
        two = int(input())

        correction = one * two
        s_to_audio(correction)

    else:
        return c


# what is the date and time today
def d_and_t():
    current = dt.datetime.now()

    s_to_audio(current.strftime("It is currently %A the %d of %Y with a current time of %I %M %p"))

    time.sleep(3)


def sync_run_of_weatherasync_x2():

    if __name__ == "__main__":
        if os.name == "nt":
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    

    async def get_forecast(location):
        async with python_weather.Client() as client:
            try:
                location = record()

                weather = await client.get(location)
                weather_descrip = weather.current.description.lower()
            
            except python_weather.exceptions.BadApiKeyError:
                return "API key is invalid"
            except python_weather.exceptions.NotFoundError:
                return f"Could not find weather information for {location}"
            
            else:
                return f"In {location}, it is {weather.current.temperature} degrees Celsius and {weather_descrip}."

    async def get_temp_only(location):
        async with python_weather.Client() as client:
            weather = await client.get(location)
            responses = [
                f"In {location}, it is {weather.current.temperature} degrees Celsius",
                f"The current temperature in {location} is {weather.current.temperature} degrees Celsius",
                f"It is currently {weather.current.temperature} degrees Celsius in {location}"
            ]
        return random.choice(responses)
    
    s_to_audio("Would you like the temperature only or the forecast too?")
    time.sleep(5)

    choice = record()

    if "only" in choice:
        asyncio.run(get_temp_only())
    
    if "both" in choice or "forecast" in choice:
        asyncio.run(get_forecast())
    


while True:
    start = question()
    print(start)

    if "coin" in start:
        coin_flip()
        time.sleep(3)
    
    elif "dice" in start:
        roll_a_dice()
        time.sleep(3)

    elif "calculator" in start:
        calculator()
        time.sleep(3)
    
    elif "date" in start or "time" in start:
        d_and_t()
        time.sleep(3)
    
    elif "weather" in start:
        sync_run_of_weatherasync_x2()
        time.sleep(3)
        
    elif "done" in start:
        break

    else:
        x = 1
        no_understand()
        time.sleep(3)