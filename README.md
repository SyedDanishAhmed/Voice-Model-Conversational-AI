# Voice-Model-Conversational-AI
Intent Classification | Entity Extraction | Speech to Text | Text to Speech 

# Entity Extraction

Extracting entities from user input

Link to flask API: 'https://dev.ird.----.com/entity-model/entity_extraction'

Input is a JSON with the following format:
{"user_input_text":"","state":"", "intent": ""}

Returns string with a json format with the structure below:
{"axes": [{"name": "plot_y", "value": "CTR"}, {"name": "plot_x", "value": "discount"}, {"name": "plot_groupby", "value": "discount"}], "filters": [{"name": "brand", "value": "upscale"}, {"name": "discount", "value": "0"}]}


# Intent Extraction

Extracting intents from user input

Link to flask API: 'https://dev.ird.----.com/intent-model/intent_extraction'

Input is a JSON with the following format:
{"user_input_text":"next","state":"welcome_screen"}

Returns a string which corresponds to the intent  


# Speech to text conversion

Conversion of audio input to text

Input parameter: Byte array (sound converted to bytes)   
Returns corresponding text


# Text to Speech conversion

Conversion of text to bytearray  
Link to flask API: 'https://dev.ird.----.com/game-orc/audio-service/text-to-speech'  
Input parameter: input text  
Returns a bytearray corresponding to the text
