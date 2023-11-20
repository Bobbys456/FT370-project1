from LM_analysis import LM_text
import pandas as pd
import os

def top_5_sentiment(company, dfq, dfa, dfp):

    def get_pos(text):
        pos = LM_text(text, verb=False, txtform = True)["% positive"]
        return pos

    def get_neg(text):
        neg = LM_text(text, verb=False, txtform = True)['% negative']
        return neg

    response_sent = dfa
    response_sent['pos'] = response_sent['text'].apply(get_pos)
    response_sent['neg'] = response_sent['text'].apply(get_neg)



    response_sent = response_sent.sort_values('pos')

    with open('data/goodnews.txt', 'w') as file: 
        out = ''
        for text in response_sent.head(5)['text']: 
            out += text + '\n'
        
        file.write(out)

    response_sent = response_sent.sort_values('neg')

    with open('data/badnews.txt', 'w') as file: 
        out = ''
        for text in response_sent.head(5)['text']: 
            out += text + '\n'
        
        file.write(out)



