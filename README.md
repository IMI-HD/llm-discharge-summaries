# Automated Generation of Discharge Summaries: Leveraging Large Language Models With Clinical Data
This repository contains the codebase used for the automated generation of discharge summaries, leveraging LLaMA3 and German clinical data.

The full-text paper detailing the methodology and results can be found at [link to paper/tbd].

## Code Components
To create the prompt we used `create_prompt.py` and to run the model `run_model.py`.
To compute our quantitative metrics we used `compute_bertscore.py` and `compute_rouge.py`. To calculate BERTScore and ROUGE means and standard deviation as well as the overall generation time we used `compute_stats.py`.
The central script to manage the entire workflow can be found in  `main.py`.

## Citation
tbd
