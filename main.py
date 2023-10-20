import re
import pandas as pd 
from earnings_questions import getQAs
import os


def main(): 
    print('done')
    parse_earnings(company = 'apple')

def parse_earnings(company): 
    dfq,dfa = getQAs(company)

    #store the results as csv to avoid redundant computation
    dfq.to_csv(os.path.join('data', company + '_questions.csv'))
    dfa.to_csv(os.path.join('data', company + '_answers.csv'))

main()


