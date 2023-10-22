from LM_analysis import LM_text
import pandas as pd

def top_5_sentiment():

    def get_pos(text):
        pos = LM_text(text)["% positive"]
        return pos

    def get_neg(text):
        neg = LM_text(text)['% negative']
        return neg

    response_sent = pd.read_csv('data\\mrna_answers.csv')
    response_sent['pos'] = response_sent['text'].apply(get_pos)
    response_sent['neg'] = response_sent['text'].apply(get_neg)

    print(response_sent.sort_values('pos')['text'].head(5))


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


