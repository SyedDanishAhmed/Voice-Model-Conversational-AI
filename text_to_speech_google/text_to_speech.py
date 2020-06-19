#!/usr/bin/env python3

'''
Title : Text to speech model
Created : Sep 20, 2018 5:00 PM
Author : Syed Danish Ahmed
This code creates a pipeline which takes in text input and converts it into bytes
'''

# Library for text to speech by google
from gtts import gTTS

import array
import os

import base64

# Importing libraries for flask API
from flask import Flask
from flask import request 
app = Flask(__name__)

# Global Constants

# English-India
LANGUAGE = 'en-IN'



def is_audio_file_present(audio_file_name_mp3):

    '''Check whether the audio file to be played already exists.

    Input parameters are the following:
    audio_file_name_mp3: Name of audio file to be searched in the given location

    Returns 1 if the file is present else 0
    '''

    # Initializing the variable
    is_audio_file_present = 0

    # Get current working directory
    path = os.getcwd()

    # Check whether the given file is already present
    for file in os.listdir(path):
        if file == audio_file_name_mp3:
            is_audio_file_present = 1

    return is_audio_file_present



@app.route('/text_to_speech', methods=['GET', 'POST'])
def generate_audio_from_text():

   '''Generate audio file from text and returns the bytearray form of the file

   Input parameters are the following:
   audio_text: Text to be converted to audio
   microphone: File name to store converted audio

   Returns the audio byte array corresponding to the text
   '''

   # Passing the text and language to the engine, 
   # here we have marked slow=False. Which tells 
   # the module that the converted audio should 
   # have a high speed

   try:
        audio_text = str(request.data)
        if audio_text is not None:
          audio_text = audio_text[1:]
   except Exception as err:
        return err.message

   #audio_text = 'my name is danish'

   audio_file_name = ''.join(e for e in audio_text if e.isalnum())[0:30]

   # Creating file name for mp3 file
   audio_file_name_mp3 = "./audio_files/" + audio_file_name + '.mp3'

   # Check whether the audio file is already present
   audio_file_exists = is_audio_file_present(audio_file_name_mp3)

   if audio_file_exists == 0:
       
       # Create the audio object
       # get_audio_obj = gTTS(text = audio_text, lang = LANGUAGE, slow = False)
       get_audio_obj = gTTS(text = audio_text)

       # Saving the converted audio in a mp3 file 
       get_audio_obj.save(audio_file_name_mp3)


   # Conversion of mp3 to audio byte array
   audio_byte_array = array.array('B')
   audio_file = open(audio_file_name_mp3, 'rb')
   audio_byte_array.fromstring(audio_file.read())

   audio_bytes = base64.b64encode(bytes(audio_byte_array))

   return audio_bytes


if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port = 5004)



'''
import requests

#url = 'http://127.0.0.1:5004/text_to_speech'

url = 'http://172.25.0.59:5004/text_to_speech'

#url = 'https://dev.ird.mu-sigma.com/text_to_speech_model/text_to_speech'

request_data = "test again"

response = requests.post(url, data=request_data)

response_text  = response.text

print(response_text)

'''