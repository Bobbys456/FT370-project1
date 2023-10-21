import re
import pandas as pd 
from earnings_questions import getQAs
from LM_analysis import LM_text
import os
import nltk

company = 'ntla'

def main():   
    dfq, dfa = parse_earnings(company)

    #create single txt docs for all text in questions and answers seperately 
    create_txt(dfq, 'q')
    create_txt(dfa, 'a')

    #performs LM analysis on answers text
    with open(os.path.join('data', 'LM', 'answers.txt')) as file: 
        text = file.read()
        LM_text(text)
        

def parse_earnings(company): 
    dfq,dfa = getQAs(company)

    #store the results as csv to avoid redundant computation
    dfq.to_csv(os.path.join('data', company + '_questions.csv'))
    dfa.to_csv(os.path.join('data', company + '_answers.csv'))

    return dfq, dfa

def create_txt(df, type):
    output = ''
    for item in df['text']: 
        output += item
    
    if type=='a': 
        with open(os.path.join('data','LM', 'answers.txt'), 'w') as file: 
            file.write(output)
    else: 
        with open(os.path.join('data','LM', 'questions.txt'), 'w') as file: 
            file.write(output)



main()


