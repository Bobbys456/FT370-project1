


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import csv
import glob
import re
import string
import sys
import datetime as dt
import MOD_Load_MasterDictionary_v2022 as LM
from gunfog import calculate_gunning_fog

LMDICT_FILE_NAME="Loughran-McDonald_MasterDictionary_1993-2021.csv"
MASTER_DICTIONARY_FILE = os.path.join('data', LMDICT_FILE_NAME)
# User defined file pointer to LM dictionary
MASTER_DICTIONARY_FILE = os.path.join('data', LMDICT_FILE_NAME)
                        #  r'G:\My Drive\SRAF\LM_Master_Dictionary\\' + \
                        #  r'Loughran-McDonald_MasterDictionary_1993-2021.csv'
# User defined output file
OUTPUT_FILE = os.path.join('data'+'LMoutput.csv')

#list of common words in negation 
negation_words = [
    "NO", "NOT", "NONE", "NOBODY", "NOTHING", "NOWHERE", 
    "NEITHER", "NOR", "NEVER", "HARDLY", "SCARCELY", "BARELY", 
    "CANNOT", "CAN'T", "DIDN'T", "DOESN'T", "WON'T", "ISN'T", 
    "AREN'T", "HAVEN'T", "HASN'T", "WASN'T", "WEREN'T", 
    "SHOULDN'T", "WOULDN'T", "COULDN'T", "MUSTN'T", "AIN'T", 
    "AIN", "AIN'T", "AINT", "NOPE", "NIL", "NIX", "NAH", 
    "NEGATIVE", "DENY", "REFUSE", "DISAPPROVE", "REJECT", 
    "OPPOSE", "PROTEST", "DISAGREE", "DISALLOW", "DISCLAIM", 
    "DOUBT", "FORBID", "FORGET", "LACK", "MINUS", "MISS", 
    "REFUSE", "DENY", "WITHOUT"
    ]

# Setup output
OUTPUT_FIELDS = ['file name', 'file size', 'number of words', '% negative', '% positive',
                 '% uncertainty', '% litigious', '% strong modal', '% weak modal',
                 '% constraining', '# of alphabetic', '# of digits',
                 '# of numbers', 'avg # of syllables per word', 'average word length', 'vocabulary', 'num to words']

lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, print_flag=True)
#lm_dictionary, _md_header, _sentiment_categories, _sentiment_dictionaries, _stopwords, _total_documents = load_masterdictionary(MASTER_DICTIONARY_FILE, print_flag=True, get_other  =True)
#print( lm_dictionary, _md_header, _sentiment_categories, _sentiment_dictionaries, _stopwords, _total_documents )



def get_data(doc):

    global lm_dictionary


    vdictionary = dict()
    _odata = [0] * 17
    total_syllables = 0
    word_length = 0

    tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words
    for index, token in enumerate(tokens):
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
            _odata[2] += 1  # word count
            word_length += len(token)
            if token not in vdictionary:
                vdictionary[token] = 1
            if lm_dictionary[token].negative: 
                if any(word in tokens[index-3: index-1] for word in negation_words) or any(word in tokens[index+1: index+2] for word in negation_words):
                    _odata[4] += 1
                else: 
                    _odata[3] += 1
            if lm_dictionary[token].positive: 
                if any(word in tokens[index-3: index-1] for word in negation_words) or any(word in tokens[index+1: index+2] for word in negation_words):
                    _odata[3] += 1
                else: 
                    _odata[4] += 1
            if lm_dictionary[token].uncertainty: _odata[5] += 1
            if lm_dictionary[token].litigious: _odata[6] += 1
            if lm_dictionary[token].strong_modal: _odata[7] += 1
            if lm_dictionary[token].weak_modal: _odata[8] += 1
            if lm_dictionary[token].constraining: _odata[9] += 1
            total_syllables += lm_dictionary[token].syllables

    _odata[10] = len(re.findall('[A-Z]', doc))
    _odata[11] = len(re.findall('[0-9]', doc))
    # drop punctuation within numbers for number count
    doc = re.sub('(?!=[0-9])(\.|,)(?=[0-9])', '', doc)
    doc = doc.translate(str.maketrans(string.punctuation, " " * len(string.punctuation)))
    _odata[12] = len(re.findall(r'\b[-+\(]?[$€£]?[-+(]?\d+\)?\b', doc))

    if _odata[2] != 0:
      _odata[13] = total_syllables / _odata[2]
      _odata[14] = word_length / _odata[2]
    
    if _odata[2] != 0 : 
        _odata[16] = _odata[12]/_odata[2]

    _odata[15] = len(vdictionary)


   

    # Convert counts to %
    if _odata[2] != 0:
      for i in range(3, 9 + 1):
          _odata[i] = (_odata[i] / _odata[2]) * 100
    # Vocabulary

    return _odata

def LM_text(df, verb, txtform = False, small=False, company=''):
    ''' Demonstrate the use of LM dictionary to compute metrics per file stored in
    '''
    if not txtform: 
        text = ''
        for item in df['text']: 
            text += item
    else: 
        text = df
    
    global OUTPUT_FIELDS

    doc = text
    doc = re.sub('(May|MAY)', ' ', doc)  # drop all May month references
    doc = doc.upper()  # for this parse caps aren't informative so shift

    # per document
    output_data = get_data(doc)

    # per document
    output_data[0] = text[0:2]
    output_data[1] = len(doc)

    #print(OUTPUT_FIELDS)
    #print(output_data)

    data = dict(zip(OUTPUT_FIELDS, output_data))

    max_key_length = max(len(key) for key in data.keys())
    
    

    if verb: 
        for key, value in data.items():
            print(f"{key:{max_key_length}} : {value}")

        print(f"{'Gunning fog index: ':{max_key_length}} : {str(calculate_gunning_fog(text))}")

        print('-'* 30)
        print('\n' * 2)

    if not small: 
        lmout = pd.DataFrame(dict(zip(OUTPUT_FIELDS, output_data)), index=[0])
        lmout.to_csv('data/LM/' +company+'_LM_output.csv')

    
    return dict(zip(OUTPUT_FIELDS, output_data))


