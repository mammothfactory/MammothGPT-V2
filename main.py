#from transformers import AutoTokenizer, AutoModelForCausalLM
#from optimum.bettertransformer import BetterTransformer
#from transformers import TrainingArguments
#import transformers
#import torch

# Offical python library with pre-defined set of classes (e.i  openai.Edit.create()) for API resources  
# https://github.com/openai/openai-python
import openai

import requests, json, re

import gradio as gr

import gradio.components as comp


# Load environment variables for usernames, passwords, & API keys
# https://pypi.org/project/python-dotenv/
from dotenv import dotenv_values

from WebApi import WebApi

#from GuiWebScraper import GuiWebScraper

MAX_CREATIVITY = 1
COLLEGE_LEVEL_CREATIVITY = 0.8
HIGH_SCHOOL_LEVEL_CREATIVITY = 0.6
ELEMENTARY_SCHOOL_LEVEL_CREATIVITY = 0.4
MIN_CREATIVITY = 0

NONE = -1
REGIRD = 0
Q_PUBLIC = 1

ENTITY_TYPES = ["Investor", "Speculator", "Land Syndicate", "Recreational Land"]
DATA_SOURCE_TYPES = ["NOT REAL TIME", "Regrid", "qPublic"]

# https://support.regrid.com/parcel-data/lbcs-keys
HOUSING_TYPES = ["1000 - Residential activities", "2000 - Shopping, business, or trade activities", "3000 - Industrial, manufacturing, and waste-related activitie", 
                 "4000 - Social, institutional, or infrastructure-related activities", "5000 - Travel or movement activities","6000 - Mass assembly of people",
                 "7000 - Leisure activities", "8000 - Natural resources-related activities", "9500 - Vacant parcel"
                 ]

model_id = "tiiuae/falcon-40b-instruct" #"tiiuae/falcon-180B"
TITLE = '🦣 Mammoth GPT'
DESCRIPTION = f'Explore the {model_id.upper()} LLM with Real Estate fine-tuning'


def ai_score() -> int: 
    # https://oneai.com/agent/2
    # https://github.com/openai/openai-python#embeddings
    # https://platform.openai.com/docs/guides/embeddings/limitations-risks   
    return 85.2


def google_search():
    """ 
    Copy the following code and paste it into your site's <body> section, where you want the search box and the search results to render.
    <script async src="https://cse.google.com/cse.js?cx=e1abcf6bceb1244e8">
    /script>
    <div class="gcse-search"></div>
    
    
    https://developers.google.com/custom-search/v1/introduction
    https://programmablesearchengine.google.com/controlpanel/overview?cx=e1abcf6bceb1244e8#programmatic-access-card
    
    """
    pass

def check_hallucinations(inputAiText: str) -> tuple:
    """" Check if property names, zip codes, and ??? match the location asked in the question
    """
    
    if "2020" in inputAiText or "2021" in inputAiText or "2022" in inputAiText:
        return False 



def find_real_time_info_ai_output(source, inputAiText, housingType):
    
    item = "elements"
    
    if "properties" in inputAiText:
        item = "properties"
        
    if "cities" in inputAiText:
        item = "cities"

    if "county" in inputAiText.lower():
        item = "county"
        
    if "state" in inputAiText.lower():
        item = "state"

    #DEBUG print(f"Using {item} to find zip codes.")
    
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": "What are possible zip codes for the {item} described in " + inputAiText}], temperature=0.2)
    zipcodes = completion.choices[0].message.content 
    print(zipcodes)  # THIS MIGHT BE BETTER AI OUTPUT AND 
    
    zipcodeList = re.findall(r'\b\d{5}\b', zipcodes)    # Locate all strings that are 5 digits long
    
    header = ""
    if source == REGIRD:
        # TODO Search within 20 miles of the following zip codes zipcodeList
        # https://support.regrid.com/parcel-data/lbcs-keys
        
        houseTypeRange = []
        if housingType == HOUSING_TYPES[0]:
            houseTypeRange = [1000, 1900]
        elif housingType == HOUSING_TYPES[1]:
            houseTypeRange = [2000, 2900]        
        
        for zipcode in zipcodeList:
            url =  WebApi.construct_regrid_url(zipcode, houseTypeRange) 
            response = requests.get(url, headers=WebApi.HEADERS)

            if response.status_code == 200 and 'application/json' in response.headers['Content-Type']:
                data = response.json()
                with open("output.json", "w") as file:
                    json.dump(data, file, indent=2)
            else:
                print(f"Failed to fetch or parse JSON. Status code: {response.status_code}")

            target_key = "parcelnumb_no_formatting"
            #print(WebApi.count_key_occurence("output.json", target_key))


            print(WebApi.get_property_details("output.json", ["parcelnumb_no_formatting", "owner"]))
                
        header = f"Using ReGrid real time data for zipcode(s) {zipcodeList} \n \n"
    
    elif source == Q_PUBLIC:
        header = f"Using qPublic real time data for zipcode(s) {zipcodeList} \n \n"
        #GuiWebScraper.start()
    
    else: 
        # https://llama-cpp-python.readthedocs.io/en/latest 
        header = "NOT using REAL TIME-DATA ..."
    
    
    return header + inputAiText #+ zipcodes


def generate(inputQuestion, entity, dataSource, inputTemperature, housingType):
    
    #DEBUG: print(f"Temp: {inputTemperature} - Question: {inputQuestion} - Entity: {entity} - Data SOurce: {dataSource}")
    
    parameters = [dataSource, inputTemperature, housingType]
    
    if "?" in inputQuestion:
        pass
    else:
        promppt = inputQuestion + "?"
    
    if entity == ENTITY_TYPES[0]:
        return llm_call(inputQuestion, parameters, "You are a land investors, please suggest properties with undeveloped land that will appreciate in value over time. ")
    elif entity == ENTITY_TYPES[1]:
        return llm_call(inputQuestion, parameters, "You are a speculators what doesn't plan to make significant improvements to the property. ")
    elif entity == ENTITY_TYPES[2]:
        return llm_call(inputQuestion, parameters, "You are in a group of investors that pooled their resources to purchase land collectively, thus spreading the risk. ")
    elif entity == ENTITY_TYPES[3]:
        return llm_call(inputQuestion, parameters, "You are looking for land for recreational purposes, such as hunting, fishing, camping, or outdoor activities. ")
    else: 
        print("No entity drop-down selected")
        return llm_call(inputQuestion, parameters)

def llm_call(prompt, parameters=[None, 0.7, HOUSING_TYPES[0]], systemRole="You are an AI Real Estate agent"):
    config = dotenv_values()
    openai.api_key = config['AI_KEY']
    
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": systemRole + prompt}], temperature=parameters[1], max_tokens=150)
    aiText = completion.choices[0].message.content
    
    if "AI language model" in aiText:
        #response = openai.Edit.create(model="text-davinci-edit-001", input=aiText, instruction="Don't use the words 'As an AI language model', in the following prompt: ", temperature=0.2)
        #aiText = response.choices[0].text.strip()
        systemRole = ""
        completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "system", "content": systemRole + "Don't use the words 'As an AI language model'. " + prompt}], temperature=0.2, max_tokens=150)
        aiText = completion.choices[0].message.content
    
    print(f"1st AI text: {aiText}")
    
    realTimeDataText = ""
    if parameters[0] == DATA_SOURCE_TYPES[0]:
        realTimeDataText = find_real_time_info_ai_output(NONE, aiText, None)
    elif parameters[0] == DATA_SOURCE_TYPES[1]:
        realTimeDataText = find_real_time_info_ai_output(REGIRD, aiText, parameters[2])
    elif parameters[0] == DATA_SOURCE_TYPES[2]:
        realTimeDataText = find_real_time_info_ai_output(Q_PUBLIC, aiText, parameters[2])
    else:
        realTimeDataText = find_real_time_info_ai_output(NONE, aiText, None)

    finalOutput = realTimeDataText
    
    return finalOutput, ai_score()


print("root@localhost:/usr/local/bin# python3 pagekite.py 6969 mgpt.pagekite.me")     
gr.Interface(fn=generate, 
             title=TITLE, description=DESCRIPTION,
             theme='gstaff/xkcd',
             inputs=[comp.Textbox(label="Input Question"),
                     comp.Dropdown(choices=ENTITY_TYPES, label="Select the type of real estate entity behavior to use:"),
                     comp.Dropdown(choices=DATA_SOURCE_TYPES, label="Use the following for the source of real-time data:"),
                     comp.Slider(label="Temperature of AI", info="Lower = More Factual", minimum=0, maximum=1, value=0.7), 
                     comp.Dropdown(choices=HOUSING_TYPES, label="What Standardized Land Use Code Keys are you searching for?:"),
                    ],
             outputs=[comp.Textbox(label="AI Output", max_lines=35),
                      comp.Textbox(label="AI Score")
                     ]
            ).launch(server_port=6969, share=False)
