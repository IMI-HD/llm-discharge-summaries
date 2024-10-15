import os

MODEL_NAME = "llama3_70b_4bit" #options: "llama3_70b_4bit" #"openbiollm_70b_4bit" #"sauerkraut_70b_4bit"

RECREATE_PROMPT = True #True: creates new prompt using EHR data; False: reads existing prompt from json-file
FILE_DIR = 'ehr_data' #location of ehr data