#!/usr/bin/env python3

'''
Title : Entity extraction
Created : Sep 10, 2018 5:00 PM
Author : Syed Danish Ahmed
This code extracts entities from user input text depending on state and intent
'''

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

import datetime

# Importing libraries for flask API
from flask import Flask
from flask import request 
app = Flask(__name__)

# Global Constants

# English-India
LANGUAGE = 'en-IN'


### Logging functions ###

# local logs
def write_local_entity_map_banner_to_segment(user_input, entity, log_file_name):

    ''' Creating a log of user text and corresponding intent

    Input parameters are the following:
    user_text: User text 
    intent: Mapping based on classification model

    Writes user text and intent into a text file
    '''

    with open(log_file_name, 'a') as log_file:
        print("{}\t{}".format(user_input, entity), file=log_file)
        return "Local log written"


# centralized logs
def write_centralized_entity_map_banner_to_segment(user_input, entity):
    entity_centralized_log_URL = "http://172.25.0.59:5014/entity-map-banner-to-segment-log"
    
    payload = {
        "user_input": user_input,
        "entity": entity
    }

    response = requests.request("POST",
                                entity_centralized_log_URL,
                                json=payload,
                                headers={'content-type': "application/json"})
    return response



def write_local_entity_user_eda(user_input, entity, log_file_name):

    ''' Creating a log of user text and corresponding intent

    Input parameters are the following:
    user_text: User text 
    intent: Mapping based on classification model

    Writes user text and intent into a text file
    '''

    with open(log_file_name, 'a') as log_file:
        print("{}\t{}".format(user_input, entity), file=log_file)
        return "Local log written"


# centralized logs
def write_centralized_entity_user_eda(user_input, entity):
    
    entity_centralized_log_URL = "http://172.25.0.59:5014/entity-user-eda-log"
    
    payload = {
        "user_input": user_input,
        "entity": entity
    }

    response = requests.request("POST",
                                entity_centralized_log_URL,
                                json=payload,
                                headers={'content-type': "application/json"})
    return response




def get_local_log_map_banner_to_segment():
    """
    Returns the name of the log file including the current date
    """
    log_file_path = "./logs/"
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)

    curr_date = datetime.datetime.today().strftime('%Y-%m-%d')
    log_file_name = "entity_local_log_map_banner_to_segment_" + curr_date + ".txt"

    return log_file_path + log_file_name


def get_local_log_user_eda():
    """
    Returns the name of the log file including the current date
    """
    log_file_path = "./logs/"
    if not os.path.exists(log_file_path):
        os.makedirs(log_file_path)

    curr_date = datetime.datetime.today().strftime('%Y-%m-%d')
    log_file_name = "entity_local_log_user_eda_" + curr_date + ".txt"

    return log_file_path + log_file_name



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



def entity_extraction_map_banner_to_segment(user_input_text):

    ''' Extracts all entities present in the user text

        Input parameter
        user_input_text: Microphone input from player

        Returns entities and their count
    '''
 
    #global entity_log_file_map_banner_to_segment

    entities = []

    entity_map = {
        "banner_name": {
            "Discount&EMI": ['emi'],
            "Discount": ['discount'],
            "Price Slash": ['price', 'slash'],
            "Cross Sale": ["cross sell", "cross sale", "castl", "chakra sale"],
            "Any": ["any banner", "any active banner"]
            },
        "segment": {
            "Family-Union": ["family", "union"],
            "Working-Class": ["working", "class"],
            "Golden-Year-Guardians": ["golden", "year", "guardian"],
            "Young-Singles" : ["young", "single"]
            }        
        }
         

    entity_score = {
        "banner_name": {
            "Discount&EMI": 0,
            "Discount": 0,
            "Price Slash": 0,
            "Cross Sale": 0,
            "Any": 0
            },
       "segment": {
            "Family-Union": 0,
            "Working-Class": 0,
            "Golden-Year-Guardians": 0,
            "Young-Singles": 0
            }        
        }
            


    # user_input_text = "visualisation of the castle banner for the click through rate"
    if user_input_text is not None:

        # Calling function for stop word removal, stemming and lemmatization
        user_input_text = text_preprocessing(str(user_input_text))

        # score the entities
        for name in entity_map['banner_name'].keys():
            for keyword in entity_map['banner_name'][name]:
                if keyword in user_input_text:
                    entity_score['banner_name'][name] += 1

        # score the entities
        for name in entity_map['segment'].keys():
            for keyword in entity_map['segment'][name]:
                if keyword in user_input_text:
                    entity_score['segment'][name] += 1


        # Initializing the output dictionery
        out = {}

        # Label for axes
        out['banner_name'] = []

        # Label for axes
        out['segment'] = []

        # Initialization for logger
        banner_name = 'NA'
        segment = 'NA'

        values = []
        if max(entity_score['banner_name'].values()) > 0:
            banner_name = max(entity_score['banner_name'].items(), key = operator.itemgetter(1))[0]
            values.append(banner_name)
            out['banner_name'].append({'name': 'banner_name','value': values})

        values = []
        for key, value in entity_score['segment'].items():
            if value > 0:
                values.append(key)
        if values:
            out['segment'].append({'name': 'segment','value': values})

        
        write_local_entity_map_banner_to_segment(user_input_text, json.dumps(out), get_local_log_map_banner_to_segment())
        write_centralized_entity_map_banner_to_segment(user_input_text, json.dumps(out))
        
        return json.dumps(out)

    else:

        # Initializing the output dictionery
        out = {}
        
        return json.dumps(out)



def entity_extraction_perform_eda(user_input_text):

    ''' Extracts all entities present in the user text

        Input parameter
        user_input_text: Microphone input from player

        Returns entities and their count
    '''

    # global entity_log_file_user_eda

    entity_map = {

    "plot_y": {
        "clickThroughRate": ["click through rate", "ctr", "kid shoe rate", "cdr", "cpr", "cbr", "cti"],
        "conversionRate": ["conver"]
            },
    "plot_x": {
        "time": ["time"],
        "productCategory": ["product", "category"],
        "activeBanner": ["banner type", "banner kind", "banner name"],
        "bannerDiscount": ["banner discount", "discount banner"],
        "bannerEmiOption": ["banner emi", "emi banner"],
        "bannerCrossSell": ["banner cross sell", "banner cross sale", "banner castl", "cross sell banner", "cross sale banner", "castl banner"],
        "bannerBrand": ["brand"],
        "segment":["segment"],
        "maritalStatus": ["marital"]
            },
    "plot_z": {
        "productCategory": ["product"],
        "activeBanner": ["banner type", "banner kind", "banner name"],
        "bannerDiscount": ["discount"],
        "bannerEmiOption": ["emi"],
        "bannerCrossSell": ["cross sell", "cross sale", "castl"],
        "bannerBrand": ["brand"],
        "segment":["segment"],
        "maritalStatus": ["marital"]
            },
    "segment": {
        "Family-Union": ["family", "union"],
        "Working-Class": ["working", "class"],
        "Golden-Year-Guardians": ["golden", "year", "guardian"],
        "Young-Singles": ["young", "singles"]
            },
    "bannerBrand": {
        "null": ["no brand"],
        "upscale": ["upscale"],
        "medium": ["medium"],
        "lowscale": ["lowscale", "low scale"]
            },
    "bannerDiscount": {
        "0": ["without discount"],
        "20": ["20 percent", "twenty percent"],
        "30": ["30 percent", "thirty percent"]
            },
    "hasDiscount": {
        "TRUE": ["with discount"]
        },
    "bannerEmiOption": {
        "false": ["without emi"],
        "true": ["with emi"]
            },
    "bannerScope": {
        "Individual": ["individual"],
        "Category": ["category"]
            },
    "maritalStatus": {
        "M": ["married"],
        "S": ["single", "unmarried"]
            },
    "activeBanner": {
        "Discount&EMI": ["for emi", "for banner emi", "is emi"],
        "Discount": ["for discount", "for banner discount", "is discount"],
        "Price Slash": ["for price", "for banner price", "is price"],
        "Cross Sale": ["for cross sell", "for cross sale", "for castl", "is cross sell", "is cross sale", "is castl"]
            }   
    }

  
    entity_score = {

    "plot_y": {
        "clickThroughRate": 0,
        "conversionRate": 0
            },
    "plot_x": {
        "time": 0,
        "productCategory": 0,
        "activeBanner": 0,
        "bannerDiscount": 0,
        "bannerEmiOption": 0,
        "bannerCrossSell": 0,
        "bannerBrand": 0,
        "segment": 0,
        "maritalStatus": 0
            },
    "plot_z": {
        "productCategory": 0,
        "activeBanner": 0,
        "bannerDiscount": 0,
        "bannerEmiOption": 0,
        "bannerCrossSell": 0,
        "bannerBrand": 0,
        "segment": 0,
        "maritalStatus": 0
            },
    "segment": {
        "Family-Union": 0,
        "Working-Class": 0,
        "Golden-Year-Guardians": 0,
        "Young-Singles": 0
            },
    "bannerBrand": {
        "null": 0,
        "upscale": 0,
        "medium": 0,
        "lowscale": 0
            },
    "bannerDiscount": {
        "0": 0,
        "20": 0,
        "30": 0
            },
    "hasDiscount": {
        "TRUE": 0
        },
    "bannerEmiOption": {
        "false": 0,
        "true": 0
            },
    "bannerScope": {
        "Individual": 0,
        "Category": 0
            },
    "maritalStatus": {
        "M": 0,
        "S": 0
            },
    "activeBanner": {
        "Discount&EMI": 0,
        "Discount": 0,
        "Price Slash": 0,
        "Cross Sale": 0
            }   
        }   


    # user_input_text = "visualisation of the castle banner for the click through rate"
    if user_input_text is not None:

        # Calling function for stop word removal, stemming and lemmatization
        user_input_text = text_preprocessing(str(user_input_text))

        # score the entities
        for name in entity_map['plot_y'].keys():
            for keyword in entity_map['plot_y'][name]:
                if keyword in user_input_text:
                    entity_score['plot_y'][name] += 1

        # score the entities
        for name in entity_map['plot_x'].keys():
            for keyword in entity_map['plot_x'][name]:
                if keyword in user_input_text:
                    entity_score['plot_x'][name] += 1

        # score the entities
        for name in entity_map['plot_z'].keys():
            for keyword in entity_map['plot_z'][name]:
                if keyword in user_input_text:
                    entity_score['plot_z'][name] += 1

        # score the entities
        for name in entity_map['segment'].keys():
            for keyword in entity_map['segment'][name]:
                if keyword in user_input_text:
                    entity_score['segment'][name] += 1

        # score the entities
        for name in entity_map['bannerBrand'].keys():
            for keyword in entity_map['bannerBrand'][name]:
                if keyword in user_input_text:
                    entity_score['bannerBrand'][name] += 1

        # score the entities
        for name in entity_map['bannerDiscount'].keys():
            for keyword in entity_map['bannerDiscount'][name]:
                if keyword in user_input_text:
                    entity_score['bannerDiscount'][name] += 1

        # score the entities
        for name in entity_map['hasDiscount'].keys():
            for keyword in entity_map['hasDiscount'][name]:
                if keyword in user_input_text:
                    entity_score['hasDiscount'][name] += 1

        # score the entities
        for name in entity_map['bannerEmiOption'].keys():
            for keyword in entity_map['bannerEmiOption'][name]:
                if keyword in user_input_text:
                    entity_score['bannerEmiOption'][name] += 1

        # score the entities
        for name in entity_map['bannerScope'].keys():
            for keyword in entity_map['bannerScope'][name]:
                if keyword in user_input_text:
                    entity_score['bannerScope'][name] += 1

        # score the entities
        for name in entity_map['maritalStatus'].keys():
            for keyword in entity_map['maritalStatus'][name]:
                if keyword in user_input_text:
                    entity_score['maritalStatus'][name] += 1

        # score the entities
        for name in entity_map['activeBanner'].keys():
            for keyword in entity_map['activeBanner'][name]:
                if keyword in user_input_text:
                    entity_score['activeBanner'][name] += 1

        # Initializing the output dictionery
        out = {}

        # Label for axes
        out['axes'] = []

        # Label for filters
        out['filters'] = []

        # Initializing for log file
        plot_x = 'NA'
        plot_y = 'NA'
        plot_z = 'NA'

        # check if plot_y is specified
        values = []
        if max(entity_score['plot_y'].values()) > 0:
            plot_y = max(entity_score['plot_y'].items(), key = operator.itemgetter(1))[0]
            values.append(plot_y)
            out['axes'].append({'name': 'plot_y','value': values})


        # check if plot_x is specified
        values = []
        if max(entity_score['plot_x'].values()) > 0:
            plot_x = max(entity_score['plot_x'].items(), key = operator.itemgetter(1))[0]
            values.append(plot_x)
            out['axes'].append({'name': 'plot_x','value': values})


        # check if plot_z is specified
        values = []
        for key, value in entity_score['plot_z'].items():
            if value > 0:
                if key != plot_x:
                    values.append(key)
                    out['axes'].append({'name': 'plot_z','value': values})
                    plot_z = key
                    break

        # check if segment is specified
        values = []
        for key, value in entity_score['segment'].items():
            if value > 0:
                if 'segment' != plot_x and 'segment' != plot_y and 'segment' != plot_z:
                    values.append(key)
        if values:                    
            out['filters'].append({'name': 'segment','value': values})

        # check if bannerBrand is specified
        values = []
        for key, value in entity_score['bannerBrand'].items():
            if value > 0:
                if 'bannerBrand' != plot_x and 'bannerBrand' != plot_y and 'bannerBrand' != plot_z:
                    values.append(key)
        if values:    
            out['filters'].append({'name': 'bannerBrand','value': values})
                    

        # check if bannerDiscount is specified
        values = []
        for key, value in entity_score['bannerDiscount'].items():
            if value > 0:
                if 'bannerDiscount' not in {plot_x, plot_y, plot_z}:
                    values.append(key)
        if values:    
            out['filters'].append({'name': 'bannerDiscount','value': values})

        # check if bannerDiscount is specified
        values = []
        for key, value in entity_score['hasDiscount'].items():
            if value > 0:
                if 'hasDiscount' not in {plot_x, plot_y, plot_z}:
                    values.append(key)
        if values:    
            out['filters'].append({'name': 'hasDiscount','value': values})

        # check if bannerEmiOption is specified
        values = []
        for key, value in entity_score['bannerEmiOption'].items():
            if value > 0:
                if 'bannerEmiOption' != plot_x and 'bannerEmiOption' != plot_y and 'bannerEmiOption' != plot_z:
                    values.append(key)
        if values:    
            out['filters'].append({'name': 'bannerEmiOption','value': values})

        # check if bannerScope is specified
        values = []
        for key, value in entity_score['bannerScope'].items():
            if value > 0:
                if 'bannerScope' != plot_x and 'bannerScope' != plot_y and 'bannerScope' != plot_z:
                    values.append(key)
        if values:    
            out['filters'].append({'name': 'bannerScope','value': values})

        # check if maritalStatus is specified
        values = []
        for key, value in entity_score['maritalStatus'].items():
            if value > 0:
                if 'maritalStatus' != plot_x and 'maritalStatus' != plot_y and 'maritalStatus' != plot_z:
                    values.append(key)
        if values:    
            out['filters'].append({'name': 'maritalStatus','value': values})

        # check if activeBanner is specified
        values = []
        for key, value in entity_score['activeBanner'].items():
            if value > 0:
                if 'activeBanner' != plot_x and 'activeBanner' != plot_y and 'activeBanner' != plot_z:
                    values.append(key)
        if values:
            out['filters'].append({'name': 'activeBanner','value': values})


        write_local_entity_user_eda(user_input_text, json.dumps(out), get_local_log_user_eda())

        write_centralized_entity_user_eda(user_input_text, json.dumps(out))
        

        return json.dumps(out)

    else:

        # Initializing the output dictionery
        out = {}
        
        return json.dumps(out)



@app.route('/entity_extraction', methods=['GET', 'POST'])
def entity_extraction():

    ''' Extracts all entities present in the user text

        Input parameter
        user_input_text: Microphone input from player

        Returns entities and their count
    '''
    out = {}
        
    entity = json.dumps(out)

    try:
    
        user_input_dict = request.get_json()

        user_input_text = str(user_input_dict['user_input_text'])

        state = str(user_input_dict['state'])

        intent = str(user_input_dict['intent'])

    except Exception as err:
        return err.message


    if user_input_text is not None and state is not None:
      
        # Storing user_input_text for logging purposes
        user_input_text_original = user_input_text

        # Calling function for stop word removal, stemming and lemmatization
        user_input_text = text_preprocessing(str(user_input_text))

        if state in ('historic_user_eda', 'live_user_eda') and intent == 'perform_eda':
            entity = entity_extraction_perform_eda(user_input_text)
        elif state in ('mission_debrief', 'introducing_banner_data_schema', 'introducing_customer_segments', 'historic_data', 'historic_user_eda', 'view_eda_results', 'design_ad_campaign', 'live_user_eda') and intent == 'map_banner_to_segment':
            entity = entity_extraction_map_banner_to_segment(user_input_text)         

        return entity



if __name__ == "__main__":

    app.run(debug=True, host='0.0.0.0', port = 5002)



'''
import array
import requests
import json


#url = 'https://dev.ird.mu-sigma.com/entity-model/entity_extraction'
url = 'http://127.0.0.1:5002/entity_extraction'

headers={'Content-Type': 'application/json'}

request_data = {"user_input_text":"visualisation ctr, conversion, time, marital and with 20 percent with emi family class, golden guardian, married, for emi, individual, upscale","state":"live_user_eda", "intent": "perform_eda"}
# {"axes": [{"name": "plot_y", "value": ["clickThroughRate"]}, {"name": "plot_x", "value": ["time"]}, {"name": "plot_z", "value": ["bannerDiscount"]}], "filters": [{"name": "segment", "value": ["Family-Union", "Working-Class", "Golden-Year-Guardians"]}, {"name": "bannerEmiOption", "value": ["1"]}, {"name": "activeBanner", "value": ["Discount&EMI", "Discount"]}]}

#request_data = {"user_input_text":"show any banner singles class","state":"live_user_eda", "intent": "map_banner_to_segment"}
# {"segment": [{"value": ["Young-singles", "Working-Class"], "name": "segment"}], "banner_name": [{"value": ["Cross Sale"], "name": "banner_name"}]}

response = requests.post(url, data=json.dumps(request_data), headers=headers)

print(response.text)
'''




