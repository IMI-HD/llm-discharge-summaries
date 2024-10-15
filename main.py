import time
import json
import os
import glob
import re
from create_prompt import create_prompt
from compute_stats import calculate_metrics, calculate_time
from config import RECREATE_PROMPT, MODEL_NAME, FILE_DIR
from run_model import generate_summary
        
def main():
    #measure generation time for all letters
    start_time_full = time.time()
    metrics_list = []
    time_list = []
      
    files = glob.glob(os.path.join(FILE_DIR, '*.txt'))
    #loop over all files in direcotry
    for file_path in files:
        #measure generation time for single letter
        start_time = time.time()
        with open(file_path, 'r') as file:
            input_ehr_data = file.read()
            #get case id
            input_id = ''.join(re.findall(r'\d+', file_path))
            
            if RECREATE_PROMPT:
                #create prompt
                prompt = create_prompt(input_ehr_data)
                #save prompt to file
                with open(f'prompts/{input_id}_prompt.json', 'w', encoding='utf-8') as json_file:
                    json.dump(prompt, json_file, indent=4, ensure_ascii=False)
            else:
                #read prompt from file
                with open(f'prompts/{input_id}_prompt.json', 'r', encoding='utf-8') as json_file:
                    prompt = json.load(json_file)
                    
            #read human summary from file (for metric calculation)
            hum_sum = ''
            with open('hum_summaries/gen_discharge_letters.json', 'r', encoding='utf-8') as json_file:
                hum_summaries = json.load(json_file)
                for item in hum_summaries:
                    if input_id in item.get('id'):
                        hum_sum = item.get('AnamneseBefund') + "\n\n" + item.get('TherapieVerlauf')
                        break
            
            #generates summary using the MODEL_NAME
            gen_summary, metrics = generate_summary(model_name=MODEL_NAME, case_id=input_id, prompt=prompt, hum_sum=hum_sum)
    
            metrics_list.append(metrics)
            end_time = time.time()
            generation_time = end_time - start_time
            time_list.append(generation_time)

    #calculate mean + std for each metric
    calculate_metrics(metrics_list)
    calculate_time(time_list)
    
    end_time_full = time.time()
    generation_time_full = end_time_full - start_time_full
    print('GENERATION TIME', generation_time_full)