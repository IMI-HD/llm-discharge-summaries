import torch
import json
import os
from transformers import LlamaForCausalLM, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from compute_bertscore import compute_bert_single
from compute_rouge import compute_rouge_single

bnb_config = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_use_double_quant=True, bnb_4bit_quant_type="nf4", bnb_4bit_compute_dtype=torch.bfloat16)

def get_result(gen_summary_with_prompt):
    #gets the reply of the model
    keyword = 'assistant'
    index = gen_summary_with_prompt.rfind(keyword) #finds the last keyword in the string
    if index != -1:
        return gen_summary_with_prompt[index + len(keyword):]
    else:
        print("keyword not found")
        return ''
    
def save_summary(gen_summary, metrics, prompt, CASE_ID, MODEL_NAME):
    #saves result as json + txt; adds a counter to the file, if a file with the same name exists already
    data = []
    data.append({'id' : CASE_ID, 'model' : MODEL_NAME, 'metrics' : metrics, 'prompt': prompt, 'gen_summary': gen_summary})
    
    ext = '.json'
    filename = f'{CASE_ID}_{MODEL_NAME}{ext}'
    counter = 2
    directory = 'results'
    
    while os.path.exists(os.path.join(directory, filename)):
        filename = f'{CASE_ID}_{MODEL_NAME}_{counter}{ext}'
        counter += 1
    
    with open(f'{directory}/{filename}', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

    #save as txt in addition
    filename = filename.split('.')[0]
    with open(f'{directory}/{filename}.txt', 'w', encoding='utf-8') as txt_file:
        txt_file.write(gen_summary)

def generate_summary(model_name, case_id, prompt, hum_sum):
    #links to corresponding model on huggingface
    model_links = {"llama3_70b_4bit": "meta-llama/Meta-Llama-3-70B-Instruct", "openbiollm_70b_4bit": "aaditya/Llama3-OpenBioLLM-70B", "sauerkraut_70b_4bit": "VAGOsolutions/Llama-3-SauerkrautLM-70b-Instruct"}
    model = LlamaForCausalLM.from_pretrained(model_links[model_name], quantization_config=bnb_config)
    tokenizer = AutoTokenizer.from_pretrained(model_links[model_name])
    
    #tokenize prompt
    input_ids = tokenizer.apply_chat_template(prompt, tokenize=True, add_generation_prompt=True, return_tensors="pt")
    print(tokenizer.decode(input_ids[0]))
    
    #move tokenized input to GPU
    input_ids = input_ids.to('cuda:0')
    
    #generate output tokens
    gen_tokens = model.generate(input_ids, do_sample=True, temperature=0.2, max_new_tokens=1000, eos_token_id=[tokenizer.eos_token_id, tokenizer.convert_tokens_to_ids("<|eot_id|>")])

    #de-tokenize output
    gen_summary_with_prompt = tokenizer.batch_decode(gen_tokens, skip_special_tokens=True, clean_up_tokenization_spaces=False)[0]
    #keep only assistant's answer
    gen_summary = get_result(gen_summary_with_prompt)
    print(gen_summary)
    
    #compute metrics
    bertscore = compute_bert_single(gen_summary, hum_sum)
    rouge = compute_rouge_single(gen_summary, hum_sum)
    metrics = {"id": case_id, "BERTScore": bertscore, "ROUGE": rouge}
    print(metrics)
    
    save_summary(gen_summary, metrics, prompt, case_id, model_name)
    
    return gen_summary, metrics