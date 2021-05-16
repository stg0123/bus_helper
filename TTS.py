"""Synthesizes speech from the input string of text or ssml.

Note: ssml must be well-formed according to:
    https://www.w3.org/TR/speech-synthesis/
    """
#from google.cloud import texttospeech

import threading as thread
from queue import Queue
import os
import time

def start(stringNum):
    bus = stringNum

    from google.cloud import texttospeech
# Instantiates a client
    client = texttospeech.TextToSpeechClient()
#sentence = input("번호 입력 : ")
#    num = sentence
    # Set the text input to be synthesized
    sentence = bus + "번 버스가 도착했습니다."
    synthesis_input = texttospeech.SynthesisInput(text=sentence)
    # Build the voice request, select the language code ("en-US") and the ssml
    # voice gender ("neutral")
    voice = texttospeech.VoiceSelectionParams(
        language_code="ko-KR", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    output = "sound" + ".wav"
    # The response's audio_content is binary.
    with open(output, "wb") as out:
    # Write the response to the output file.
        out.write(response.audio_content)
#        print('Audio content written to file' + output)

    os.system('omxplayer sound.wav')

    
    
def tts (q) :
    while True :
        if q.empty() == False :
            tmp = q.get()
            start(tmp)

#q = Queue()

#thr = thread.Thread(target= tts, args= (q,), daemon= True)
#thr.start()

#a = input("input bus num : ")
#q.put(a)
#b = '378'
#q.put(b)
#tts(q)
