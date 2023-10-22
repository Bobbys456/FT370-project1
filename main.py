import re
import pandas as pd 
from earnings_questions import getQAs
from LM_analysis import LM_text
import os
import nltk



company = 'mrna'

def main():   

    #gets dataframes of text ans stores them to csv for debugging
    #dfq, dfa, dfp = parse_earnings(company)

    #gets dataframes without storing as csv 
    dfq,dfa, dfp = getQAs(company)

    #splitting cfo and ceo answers
    dfa['title'] = dfa['title'].apply(title_norm)
    ceo = dfa[dfa['title'] == 'CEO']
    cfo = dfa[dfa['title'] == 'CFO'] 

    print(cfo)

    #create single txt docs for all text in questions and answers seperately to be analyzed as single block of text
    create_txt(dfq, 'q')
    create_txt(dfa, 'a')
    create_txt(dfp, 'p')
    create_txt(ceo, 'c')
    create_txt(cfo, 'f')
    

    #performs analysis on answers text
    with open(os.path.join('data', 'LM', 'answers.txt')) as file: 
        print('Answers\n')
        text = file.read()
        LM_text(text)
        
    
    #performs analysis on prepared remakrs text
    with open(os.path.join('data', 'LM', 'prepared_remarks.txt')) as file: 
        print('Prepared Remarks\n')
        text = file.read()
        LM_text(text)
    
    with open(os.path.join('data', 'LM', 'cfo.txt')) as file: 
        print('CFO answers\n')
        text = file.read()
        LM_text(text)

    with open(os.path.join('data', 'LM', 'ceo.txt')) as file: 
        print('CEO answers\n')
        text = file.read()
        LM_text(text)
    
        

def parse_earnings(company): 
    dfq,dfa, dfp = getQAs(company)

    #store the results as csv to avoid redundant computation
    dfq.to_csv(os.path.join('data', company + '_questions.csv'))
    dfa.to_csv(os.path.join('data', company + '_answers.csv'))
    dfp.to_csv(os.path.join('data', company + '_prepared.csv'))

    return dfq, dfa, dfp

def create_txt(df, type):
    output = ''
    for item in df['text']: 
        output += item
    
    if type=='a': 
        with open(os.path.join('data','LM', 'answers.txt'), 'w') as file: 
            file.write(output)
    elif type =='q': 
        with open(os.path.join('data','LM', 'questions.txt'), 'w') as file: 
            file.write(output)
    elif type =='c': 
        with open(os.path.join('data','LM', 'ceo.txt'), 'w') as file: 
            file.write(output)
    elif type =='f': 
        with open(os.path.join('data','LM', 'cfo.txt'), 'w') as file: 
            file.write(output)
    else: 
        with open(os.path.join('data','LM', 'prepared_remarks.txt'), 'w') as file: 
            file.write(output)

def title_norm(text): 
    if ('Chief Executive Officer' or 'President') in text:  
        return 'CEO'
    elif 'Chief Financial Officer' in text: 
        return 'CFO'
    else: 
        return text
    
def get_pos(text):
    pos = LM_text(text)["% positive"]
    return pos

def get_neg(text):
    neg = LM_text(text)['% negative']
    return neg

main()


