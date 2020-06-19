#!/usr/bin/env python3

'''
Title : Voice model pipeline
Created : Jul 27, 2018 5:00 PM
Author : Syed Danish Ahmed
This code creates a pipeline for handling microphone audio transcriptions
Revisions : Added name extraction
Version : 0.1
Date : Jul 30, 2018 06:00 PM
Author : Syed Danish Ahmed
Changes : Added python queue for storing user inputs
Version : 0.2
Date : Jul 31, 2018 1:00 PM
Author : Syed Danish Ahmed
Changes : Added multiprocessing
Version : 0.3
Date : Aug 08, 2018 3:00 PM
Author : Syed Danish Ahmed
Changes : Removed queue and multiprocessing
Date : Aug 21, 2018 6:00 PM
Author : Syed Danish Ahmed
Changes : Modularized the code further
Date : Aug 31, 2018 6:00 PM
Author : Syed Danish Ahmed
Changes : Modified to work as flask voice model

'''

# Importing in-buit python modules


# Importing required libraries
import speech_recognition as sr

# Importing libraries for flask API
from flask import Flask
from flask import request 
app = Flask(__name__)

# Global Constants

# English-India
LANGUAGE = 'en-IN'

#https://cloud.google.com/speech-to-text/docs/encoding

def recognize_speech_from_ui(audio):

    '''Takes an AudioData object of type speech_recognition
        and returns the transcription 

    Input parameters are the following:
    "audio": AudioData object of type speech_recognition


    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    '''

    print('recognize_speech_from_ui called')

    # Creating objects for recognizer and microphone
    recognizer_obj = sr.Recognizer()


    # operation_timeout represents the timeout (in seconds) 
    # for internal operations, such as API requests

    recognizer_obj.operation_timeout = 10

    # energy_threshold adjusts the energy threshold dynamically using audio 
    # from source (an AudioSource instance) to account for ambient noise.
    # Values below this threshold are considered silence, 
    # and values above this threshold are considered speech.
    # Typical values for a silent room are 0 to 100, 
    # and typical values for speaking are between 150 and 3500.

    recognizer_obj.energy_threshold = 200

    # pause_threshold represents the minimum length of silence (in seconds) 
    # that will register as the end of a phrase

    #recognizer_obj.pause_threshold = 0.8


    # timeout parameter is the maximum number of seconds that this will 
    # wait for a phrase to start before giving up and throwing an 
    # speech_recognition.WaitTimeoutError exception. If timeout is None, 
    # there will be no wait timeout.

    timeout = 7

    # phrase_time_limit parameter is the maximum number of seconds that 
    # this will allow a phrase to continue before stopping and returning 
    # the part of the phrase processed before the time limit was reached

    phrase_time_limit = 10

    # duration: You can adjust the time-frame that adjust_for_ambient_noise() 
    # uses for analysis with the duration keyword argument

    duration = 1


    # Key values for different APIs
    #WIT_AI_KEY = "XUNWFDDXXFNEOH2YJGMTUGOCDFW33ORH"
    WIT_AI_KEY = "HTVK3WZYUIXJZT5FFMTWQE3LS6UWVZBG"
    BING_KEY = "237045f55cd641848bcd6436c9ee5c24"


    # check that recognizer and microphone parameters are appropriate type
    if not isinstance(recognizer_obj, sr.Recognizer):
        raise TypeError("`recognizer` must be `Recognizer` instance")


     # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }

        
    # try recognizing the speech in the recording
    # if a RequestError or UnknownValueError exception is caught,
    #     update the response object accordingly

    try:
        #response["transcription"] = recognizer_obj.recognize_bing(audio, key = BING_KEY, language = LANGUAGE)
        response["transcription"] = recognizer_obj.recognize_google(audio, language = LANGUAGE)
        #response["transcription"] = recognizer_obj.recognize_wit(audio, key=WIT_AI_KEY, language = LANGUAGE)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    except sr.WaitTimeoutError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "WaitTimeoutError"
    #except timeout:    
        #response["success"] = False
        #response["error"] = "API timeout"
    except Exception:    
        response["success"] = False
        response["error"] = "exception"

    print("success: ", response["success"])
    print("error: ", response["error"])
    print("transcription: ", response["transcription"])

    return response



@app.route('/audio_consumer', methods=['GET', 'POST'])
def user_input_consumer():

    ''' Consumes input in the form of audio array 
        and returns the corresponding text

        Input parameters are the following:
        audio_byte_array: audio with type bytearray

        Returns either of the three below:
        "user_input_text"            : text obtained from audio input
        "unable_to_recognize_speech" : message if recognizer could not recognize speech
        "api_unavailable"            : message if recognizer api is unavailable 


    '''

    # Converting input to bytearray format
    audio_byte_array = bytearray(request.data)

    # Converting input to type speech_recognition's AudioData
    # Sample 
    #audio = sr.AudioData(audio_byte_array, 24000, 2)
    audio = sr.AudioData(audio_byte_array, 24000, 2)

    # Calling function to get text from audio
    user_mic_input = recognize_speech_from_ui(audio)

  
    # Check whether api is working and transcription is successful
    if user_mic_input["success"] == True and user_mic_input["error"] == None:

        # Calling module for intent extraction
        user_input_text = str(user_mic_input["transcription"].lower())

        return user_input_text

    # Check whether api is working and transcription was not successful
    elif user_mic_input["success"] == True and user_mic_input["error"]:
        
        return  "unable_to_recognize_speech"

    # Check whether api is not working
    elif user_mic_input["success"] == False:
        
        return  "api_unavailable"



if __name__ == "__main__":

    # Code to run flask app
    # app.run(debug=True)

    app.run(debug=True, host='0.0.0.0', port = 5000)


''' Code to call this service


import array
import requests

#url = 'http://127.0.0.1:5001/intent_extraction'
#url = 'http://127.0.0.1:5001/entity_extraction'
#url = 'http://172.25.0.59:5000/audio_consumer'
#url = 'https://dev.ird.mu-sigma.com/voice-model/audio_consumer'

url = 'http://172.25.2.141:5003/audio_consumer'

audio_byte_array = array.array('B')
audio_file = open("/home/syed/Desktop/MixedReality/codes/audio_capture_experiments/HelloHelloHello.wav", 'rb')

#audio_file = open("HelloHelloHello.wav", 'rb')

audio_byte_array.fromstring(audio_file.read())

#request_data = {"byte_array": audio_byte_array, 
#                "test": "test_string"}

# response = requests.post(url, data=request_data, headers={'Content-Type': 'application/octet-stream'})
response = requests.post(url, data=audio_byte_array, headers={'Content-Type': 'application/octet-stream'})

print(response.text)

'''


