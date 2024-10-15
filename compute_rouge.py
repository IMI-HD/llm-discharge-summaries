from rouge import Rouge 

#compute rouge score
def compute_rouge_single(hypothesis, reference):
    rouge = Rouge()
    return rouge.get_scores(hypothesis, reference)