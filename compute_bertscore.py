from bert_score.scorer import BERTScorer

def compute_bert_single(hypothesis, reference, proxies):
    scorer = BERTScorer(model_type="facebook/bart-large-mnli")
    pr, re, f1 = scorer.score([hypothesis], [reference])
    bertscore = {'r': re.tolist()[0], 'p': pr.tolist()[0], 'f': f1.tolist()[0]}

    return bertscore