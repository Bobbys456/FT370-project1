import re
import pandas as pd 
from earnings_preprocess import getQAs
from LM_analysis import LM_text
import os
import nltk
from sentiment import top_5_sentiment





def analyze_call(company, storedata=False):   

        #gets dataframes of text ans stores them to csv for debugging
    if storedata: 
        dfq, dfa, dfp = parse_earnings(company)
    else: 
        #gets dataframes without storing as csv 
        dfq,dfa, dfp = getQAs(company, storedata)
        
    print("text split.....\n\n\n")

    #splitting cfo and ceo answers
    dfa['title'] = dfa['title'].apply(title_norm)
    ceo = dfa[dfa['title'] == 'CEO']
    cfo = dfa[dfa['title'] == 'CFO'] 

    print("cfo and ceo split.....\n\n\n")

    #create single txt docs for all text in questions and answers seperately to be analyzed as single block of text
    if storedata: 
        create_txt(dfq, 'q')
        create_txt(dfa, 'a')
        create_txt(dfp, 'p')
        create_txt(ceo, 'c')
        create_txt(cfo, 'f')
    

    #performs analysis on answers text
    print(company + ': All answers\n')
    LM_text(dfa, True)
    
        
    #performs analysis on prepared remakrs text
    print(company + ': Prepared remarks\n')
    LM_text(dfp, True)
    
    #analysis on cfo answers
    print(company + ': CFO answers\n')
    LM_text(cfo, True)

    #analysis on ceo answers
    print(company + ': CEO answers\n')
    LM_text(ceo, True)

    #Generates to text files, good and bad news, that contain the top 5 text peices for positiveand negative sentiment
    top_5_sentiment(company, dfq, dfa, dfp) 
    
        

def parse_earnings(company): 
    dfq,dfa, dfp = getQAs(company)

    #store the results as csv to avoid redundant computation
    dfq.to_csv(os.path.join('data', company + '_questions.csv'))
    dfa.to_csv(os.path.join('data', company + '_answers.csv'))
    dfp.to_csv(os.path.join('data', company + '_prepared.csv'))

    return dfq, dfa, dfp

def create_txt(df, type, company):
    output = ''
    for item in df['text']: 
        output += item
    
    if type=='a': 
        with open(os.path.join('data','LM', company + '_answers.txt'), 'w') as file: 
            file.write(output)
    elif type =='q': 
        with open(os.path.join('data','LM',  company + '_questions.txt'), 'w') as file: 
            file.write(output)
    elif type =='c': 
        with open(os.path.join('data','LM',  company + '_ceo.txt'), 'w') as file: 
            file.write(output)
    elif type =='f': 
        with open(os.path.join('data','LM',  company + '_cfo.txt'), 'w') as file: 
            file.write(output)
    else: 
        with open(os.path.join('data','LM',  company + '_prepared_remarks.txt'), 'w') as file: 
            file.write(output)

def title_norm(text): 
    if ('Chief Executive Officer' or 'President') in text:  
        return 'CEO'
    elif 'Chief Financial Officer' in text: 
        return 'CFO'
    else: 
        return text
    
def get_pos(text):
    pos = LM_text(text, False)["% positive"]
    return pos

def get_neg(text):
    neg = LM_text(text, False)['% negative']
    return neg




