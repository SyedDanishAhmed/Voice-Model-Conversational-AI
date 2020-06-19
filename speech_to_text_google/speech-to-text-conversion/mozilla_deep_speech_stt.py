'''Connect to Bernard Server

$ ssh bernard@172.25.2.141
password: arnold

Activate virtual environment using:
$ source ~/mozilla_deepspeech/mozilla_stt_py2/bin/activate

$ cd ~/mozilla_deepspeech/DeepSpeech/

'''

# f = open("my_audio.wav", "wb")

# audio_byte_array = array.array('B')

# audio_file = open("/home/syed/Desktop/MixedReality/codes/audio_capture_experiments/HelloHelloHello.wav", 'rb')
# audio_byte_array.fromstring(audio_file.read())

# f.write(audio_byte_array)


from flask import Flask
from flask import request
import array
#import requests

app = Flask(__name__)
import subprocess
import os


@app.route('/audio_consumer', methods=['GET', 'POST'])
def user_input_consumer():	
	
	# Converting input to bytearray format
	audio_byte_array = bytearray(request.data)  

	# # Read audio_byte_array from a wav file
	# audio_byte_array = array.array('B')
	# audio_file = open("/home/bernard/mozilla_deepspeech/DeepSpeech/test_audio/my_audio.wav", 'rb')
	# audio_byte_array.fromstring(audio_file.read())
	# audio_file.close()

	f = open("/home/bernard/mozilla_deepspeech/DeepSpeech/test_audio/my_audio.wav", "wb")

	f.write(audio_byte_array)

	# Variable to store audio file name (without .wav extension)
	my_audio = "my_audio"

	# Changing frequency of input audio file to 16000 Hz
	# hz_change = "ffmpeg -i ~/mozilla_deepspeech/DeepSpeech/test_audio/my_audio.wav -ar 16000 ~/mozilla_deepspeech/DeepSpeech/test_audio/my_audio_16hz.wav"
	hz_str1 = "ffmpeg -i ~/mozilla_deepspeech/DeepSpeech/test_audio/"
	hz_str2 = ".wav -ar 16000 ~/mozilla_deepspeech/DeepSpeech/test_audio/"
	hz_str3 = "_16hz.wav"
	hz_change = hz_str1 + my_audio + hz_str2 + my_audio + hz_str3
	#remving previous file
	os.system("rm -r /home/bernard/mozilla_deepspeech/DeepSpeech/test_audio/my_audio_16hz.wav")
	os.system(hz_change)

	# Running deepspeech
	# ds_model = "deepspeech models/output_graph.pb test_audio/my_audio_16hz.wav models/alphabet.txt models/lm.binary models/trie"
	ds_str1 = "deepspeech ~/mozilla_deepspeech/DeepSpeech/models/output_graph.pb ~/mozilla_deepspeech/DeepSpeech/test_audio/"
	ds_str2 = "_16hz.wav ~/mozilla_deepspeech/DeepSpeech/models/alphabet.txt ~/mozilla_deepspeech/DeepSpeech/models/lm.binary ~/mozilla_deepspeech/DeepSpeech/models/trie"
	ds_model = ds_str1 + my_audio + ds_str2 + ">" + my_audio + ".txt"
	os.system(ds_model)

	output_text = open("my_audio.txt", "r")
	file_contents = output_text.read()
	file_contents = str(file_contents)
	#print(file_contents)
	output_text.close()

	return file_contents

	

if __name__ == "__main__":

    # Code to run flask app
    app.run(debug=True, host='0.0.0.0', port = 5003)