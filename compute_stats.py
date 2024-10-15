import statistics
import json

OUTPUT_FILENAME = 'stats.png'

def calculate_metrics(metrics):
    #save metrics to file
    with open('metrics.json', 'w', encoding='utf-8') as json_file:
        json.dump(metrics, json_file, indent=4, ensure_ascii=False)
    
    #get scores from file
    bertscores = [item["BERTScore"]["f"] for item in metrics]
    rouges1 = [item["ROUGE"][0]["rouge-1"]["f"] for item in metrics]
    rouges2 = [item["ROUGE"][0]["rouge-2"]["f"] for item in metrics]
    rougesl = [item["ROUGE"][0]["rouge-l"]["f"] for item in metrics]
    
    #get mean + std of each score
    bert_mean = statistics.mean(bertscores)
    bert_std = statistics.stdev(bertscores)
    
    rouge1_mean = statistics.mean(rouges1)
    rouge1_std = statistics.stdev(rouges1)
    rouge2_mean = statistics.mean(rouges2)
    rouge2_std = statistics.stdev(rouges2)
    rougel_mean = statistics.mean(rougesl)
    rougel_std = statistics.stdev(rougesl)
    
    metrics_calc = {
        "BERTScore": {"mean": bert_mean, "std_dev": bert_std},
        "ROUGE": {"ROUGE-1": {"mean": rouge1_mean, "std_dev": rouge1_std}, "ROUGE-2": {"mean": rouge2_mean, "std_dev": rouge2_std}, "ROUGE-L": {"mean": rougel_mean, "std_dev": rougel_std}},
        }
    print(metrics_calc)
    
    with open("metrics_calc.json", 'w') as json_file:
        json.dump(metrics_calc, json_file, indent=4, ensure_ascii=False)
        
def calculate_time(times):
    #get mean + std of generation time
    time_mean = statistics.mean(times)
    time_std = statistics.stdev(times)
    print(f'TIMES - Mean: {time_mean}, Std Dev: {time_std}')
    
    times_calc = {"Mean": time_mean, "Std Dev": time_std}
    with open("times_calc.json", 'w') as json_file:
        json.dump(times_calc, json_file, indent=4, ensure_ascii=False)
        
    with open("times.json", 'w') as json_file:
        json.dump(times, json_file, indent=4, ensure_ascii=False)