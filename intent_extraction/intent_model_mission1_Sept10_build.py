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
'''

# List of states
# 1. welcome_screen
# 2. choose_your_role
# 3. narrative_empathise
# 4. narrative_scenario
# 5. select_mission
# 6. introducing_banner_data_schema
# 7. introducing_customer_segments
# 8. introducing_historic_data_and_sample_eda_query
# 9. user_eda
# 10. view_eda_results
# 11. design_ad_campaign

# Importing in-buit python modules

# Library for json operations
import json

from numpy import argmax

# Importing library for nlp functionalities
import nltk
# Importing the corpus of stopwords from nltk
from nltk.corpus import stopwords

from nltk.stem import WordNetLemmatizer 
from nltk.stem.porter import PorterStemmer

lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

import operator

import requests

import os

import ast


# Importing libraries for flask API
from flask import Flask
from flask import request 
app = Flask(__name__)

from flask import jsonify

# Global Constants

# English-India
LANGUAGE = 'en-IN'

def intent_write_log(user_text, intent, intent_log_file):
    f = open(intent_log_file, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\t{}".format(user_text, intent))  # write the text to the logfile and move to next line
    return

def entity_write_log(
	user_text, user_input_text, banner, metric, customer_segment, customer_demographic_attribute, product_category, brand_sensitivities, discounts, timeline, entity_log_file):
    f = open(entity_log_file, 'a')           # 'a' will append to an existing file if it exists
    f.write("{}\t{}".format(user_text, user_input_text, banner, metric, customer_segment, customer_demographic_attribute, product_category, brand_sensitivities, discounts, timeline, entity_log_file))  # write the text to the logfile and move to next line
    return


def text_preprocessing(user_input_text):

    # # Getting the list of english stop words from nltk library
    # stop = stopwords.words('english')

    # # List of additional stopwords
    # #newStopWords = ['name']

    # # Extending the list of existing stopwords
    # #stop.extend(newStopWords)

    # # Stop word removal
    # user_input_text = ' '.join([i for i in user_input_text.split() if i not in stop])
    # # Lemmatization
    # user_input_text = " ".join([lemmatizer.lemmatize(word) for word in user_input_text.split()])
    # # Stemming
    # user_input_text = " ".join([stemmer.stem(word) for word in user_input_text.split()])

    return user_input_text



def intent_extraction_welcome_screen(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''

    user_intent = 'not_applicable'

    # List of keywords to identify whether game is to be started
    keywords = ['next']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'go_ahead'

    # List of keywords to identify whether game is to be started
    keywords = ['exit']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'exit_game'

    # Returns the identified intent
    return user_intent



def intent_extraction_choose_your_role(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''
    user_intent = 'not_applicable'

    # List of keywords to identify whether game is to be started
    keywords = ['next']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'go_ahead'

    # List of keywords to identify whether game is to be started
    keywords = ['exit']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'exit_game'

    # Returns the identified intent
    return user_intent


def intent_extraction_narrative_empathise(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''

    user_intent = 'not_applicable'

    # List of keywords to identify whether game is to be started
    keywords = ['next']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'go_ahead'

    # List of keywords to identify whether game is to be started
    keywords = ['exit']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'exit_game'

    # Returns the identified intent
    return user_intent



def intent_extraction_narrative_scenario(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''

    user_intent = 'not_applicable'

    # List of keywords to identify whether game is to be started
    keywords = ['next']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'go_ahead'

    # List of keywords to identify whether game is to be started
    keywords = ['exit']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'exit_game'

    # Returns the identified intent
    return user_intent



def intent_extraction_select_mission(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''

    user_intent = 'not_applicable'

    # List of keywords to identify whether game is to be started
    keywords = ['black', 'friday', 'prepare', 'next']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'go_ahead'

    # List of keywords to identify whether game is to be started
    keywords = ['exit']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'exit_game'

    # Returns the identified intent
    return user_intent


def intent_extraction_introducing_banner_data_schema(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''
    user_intent = 'not_applicable'

    # List of keywords to identify whether game is to be started
    keywords = ['explore', 'banner']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'explore_banners'

    # List of keywords to identify whether game is to be started
    keywords = ['next']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'go_ahead'

    # List of keywords to identify whether game is to be started
    keywords = ['exit']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'exit_game'

    # Returns the identified intent
    return user_intent


def intent_extraction_introducing_customer_segments(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''
    user_intent = 'not_applicable'

    # List of keywords to identify whether game is to be started
    keywords = ['customer', 'segment', 'visual']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'visualize_customer_segment'

    # List of keywords to identify whether game is to be started
    keywords = ['begin', 'black', 'friday', 'next']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'go_ahead'

    # List of keywords to identify whether game is to be started
    keywords = ['exit']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'exit_game'

    # Returns the identified intent
    return user_intent



def intent_extraction_introducing_historic_data_and_sample_eda_query(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''
    user_intent = 'not_applicable'

    # List of keywords to identify whether game is to be started
    keywords = ['next']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'go_ahead'

    # List of keywords to identify whether game is to be started
    keywords = ['see', 'more']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'see_more_sample_eda_query'

    # List of keywords to identify whether game is to be started
    keywords = ['exit']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'exit_game'

    # Returns the identified intent
    return user_intent



def intent_extraction_user_eda(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''
    user_intent = 'not_applicable'

    # # List of keywords to identify whether game is to be started
    # keywords = ['next']

    # # Check whether start game keyword present in user_input_text
    # for word in keywords:
    #     if word in user_input_text:
    #         user_intent = 'go_ahead'

    # List of keywords to identify whether game is to be started
    keywords = ['visual', 'graph', 'chart', 'plot', 'univariate', 'bivariate', 'correlation', 'matrix', 'show', 'variation', 'metric', 'variance', 'vary', 'draw', 'change', 'versus', 'between', 'map', 'compare', 'view', 'measure', 'analyze']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'perform_eda'

    # List of keywords to identify whether game is to be started
    keywords = ['show', 'map']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'map_banner_to_segment'


    # # List of keywords to identify whether game is to be started
    # keywords = ['back']

    # # Check whether start game keyword present in user_input_text
    # for word in keywords:
    #     if word in user_input_text:
    #         user_intent = 'back_to_sample_query'

    # List of keywords to identify whether game is to be started
    keywords = ['exit']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'exit_game'


    # Returns the identified intent
    return user_intent



def intent_extraction_view_eda_results(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''
    user_intent = 'not_applicable'

    # List of keywords to identify whether game is to be started
    keywords = ['next']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'go_ahead'

    # List of keywords to identify whether a visualization is required
    keywords = ['pin']

    # Check whether visualization keyword present in user_input_text
    for word in keywords: 
        if word in user_input_text: 
            user_intent = 'pin_visualization'

    # List of keywords to identify whether a visualization is required
    keywords = ['try', 'new', 'query']

    # Check whether visualization keyword present in user_input_text
    for word in keywords: 
        if word in user_input_text: 
            user_intent = 'try_new_query'


    # List of keywords to identify whether game is to be started
    keywords = ['exit']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'exit_game'


    # Returns the identified intent
    return user_intent


def intent_extraction_design_ad_campaign(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''
    user_intent = 'not_applicable'

    # List of keywords to identify whether game is to be started
    keywords = ['show', 'map']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'map_banner_to_segment'

    # List of keywords to identify whether game is to be started
    keywords = ['save']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'campaign_designed_successfully'

    # List of keywords to identify whether game is to be started
    keywords = ['begin black']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'begin_black_friday'

    # List of keywords to identify whether game is to be started
    keywords = ['show', 'map']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'map_banner_to_segment'


    # List of keywords to identify whether game is to be started
    keywords = ['exit']

    # Check whether start game keyword present in user_input_text
    for word in keywords:
        if word in user_input_text:
            user_intent = 'exit_game'


    # Returns the identified intent
    return user_intent


def intent_extraction_small_talk(user_input_text):

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent

    '''
    user_intent = 'not_applicable'

    # User input text as payload
    user_input_payload = { "q": user_input_text}

    # Convert to string
    json_data = json.dumps(user_input_payload)

    # URL for intent response service for small talk
    url = 'https://qa.ird.mu-sigma.com/smalltalkbackend/parse'

    # API call for intent response service
    response = requests.request("POST", url, data=json_data, headers={'content-type': "application/json"})

    # Converting to json object
    api_response = response.json()

    # Check whether the API call was successful
    if str(response.status_code) == '200':
        user_intent = str(api_response['intent']['name'])
    else:
        user_intent = 'api_failure'

    # Returns the identified intent
    return user_intent


@app.route('/intent_extraction', methods=['GET', 'POST'])
def intent_extraction():

    '''Entity and intent extraction from text input

    Input parameters are the following:
    user_input_text: User input as text
    
    Returns the following:
    user_intent: User's intent
    '''

    #user_input_text = request.data

    #user_input_text = request.get_json()

    '''
    user_input_dict = request.form

    user_input_dict = json.dumps(user_input_dict)

    user_input_dict = ast.literal_eval(user_input_dict)

    user_input_text = str(user_input_dict['user_input_text'])

    state = int(user_input_dict['state'])

    '''

    try:

        user_input_dict = request.get_json()

        user_input_text = str(user_input_dict['user_input_text'])

        state = str(user_input_dict['state'])

    except Exception as err:
        return err.message


    global intent_log_file
    # Creating an empty list
    user_intent = 'not_applicable'

    if user_input_text is not None and state is not None:
      
        # Storing user_input_text for logging purposes
        user_input_text_original = user_input_text

        # Calling function for stop word removal, stemming and lemmatization
        user_input_text = text_preprocessing(str(user_input_text))

        if state == 'welcome_screen':
            user_intent = intent_extraction_welcome_screen(user_input_text)
        elif state == 'choose_your_role':
            user_intent = intent_extraction_choose_your_role(user_input_text)
        elif state == 'narrative_empathise':
            user_intent = intent_extraction_narrative_empathise(user_input_text)
        elif state == 'narrative_scenario':
            user_intent = intent_extraction_narrative_scenario(user_input_text)
        elif state == 'select_mission':
            user_intent = intent_extraction_select_mission(user_input_text)
        elif state == 'introducing_banner_data_schema':
            user_intent = intent_extraction_introducing_banner_data_schema(user_input_text)
        elif state == 'introducing_customer_segments':
            user_intent = intent_extraction_introducing_customer_segments(user_input_text)
        elif state == 'introducing_historic_data_and_sample_eda_query':
            user_intent = intent_extraction_introducing_historic_data_and_sample_eda_query(user_input_text)
        elif state == 'user_eda':
            user_intent = intent_extraction_user_eda(user_input_text)
        elif state == 'view_eda_results':
            user_intent = intent_extraction_view_eda_results(user_input_text)
        elif state == 'design_ad_campaign':
            user_intent = intent_extraction_design_ad_campaign(user_input_text)
        else:
            user_intent = 'not_applicable'

    # If no intent identified
    if not user_intent:
        user_intent = 'not_applicable'

    #intent_write_log(user_input_text_original, user_intent, intent_log_file)

    # Returns the identified intent
    return user_intent


if __name__ == "__main__":


    print('Game Starts!')

    #os.chdir("logs")

    #global intent_log_file, entity_log_file
    #intent_log_file = os.path.abspath(os.curdir) + "/intent.txt"
    #entity_log_file = os.path.abspath(os.curdir) + "/entity.txt"

    app.run(debug=True, host='0.0.0.0', port = 5001)




'''

import array
import requests
import json

url = 'http://127.0.0.1:5001/intent_extraction'

#url = 'https://dev.ird.mu-sigma.com/intent-model/intent_extraction'

headers={'Content-Type': 'application/json'}

#request_data = {"user_input_text":"next","state":"welcome_screen"}

#request_data = {"user_input_text":"next","state":"choose_your_role"}

#request_data = {"user_input_text":"next","state":"narrative_empathise"}

#request_data = {"user_input_text":"next","state":"narrative_scenario"}

#request_data = {"user_input_text":"next","state":"select_mission"}

#request_data = {"user_input_text":"explore","state":"introducing_banner_data_schema"}

#request_data = {"user_input_text":"visual","state":"introducing_customer_segments"}

#request_data = {"user_input_text":"visual","state":"user_eda"}

request_data = {"user_input_text":"show","state":"user_eda"}

response = requests.post(url, data=json.dumps(request_data), headers=headers)

print(response.text)

'''



# # begin black friday
# # analysis and mapping

# add next from 1 to 7
# 1-7 amd 9

# user_eda --> remove back and go go_ahead

# map intent goes to user_eda
