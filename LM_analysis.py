


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

LMDICT_FILE_NAME="Loughran-McDonald_MasterDictionary_1993-2021.csv"
MASTER_DICTIONARY_FILE = os.path.join('data', LMDICT_FILE_NAME)
# User defined file pointer to LM dictionary
MASTER_DICTIONARY_FILE = os.path.join('data', LMDICT_FILE_NAME)
                        #  r'G:\My Drive\SRAF\LM_Master_Dictionary\\' + \
                        #  r'Loughran-McDonald_MasterDictionary_1993-2021.csv'
# User defined output file
OUTPUT_FILE = os.path.join('data'+'LMoutput.csv')

# Setup output
OUTPUT_FIELDS = ['file name', 'file size', 'number of words', '% negative', '% positive',
                 '% uncertainty', '% litigious', '% strong modal', '% weak modal',
                 '% constraining', '# of alphabetic', '# of digits',
                 '# of numbers', 'avg # of syllables per word', 'average word length', 'vocabulary']

lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, print_flag=True)
#lm_dictionary, _md_header, _sentiment_categories, _sentiment_dictionaries, _stopwords, _total_documents = load_masterdictionary(MASTER_DICTIONARY_FILE, print_flag=True, get_other  =True)
#print( lm_dictionary, _md_header, _sentiment_categories, _sentiment_dictionaries, _stopwords, _total_documents )



def get_data(doc):

    global lm_dictionary


    vdictionary = dict()
    _odata = [0] * 16
    total_syllables = 0
    word_length = 0

    tokens = re.findall('\w+', doc)  # Note that \w+ splits hyphenated words
    for token in tokens:
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
            _odata[2] += 1  # word count
            word_length += len(token)
            if token not in vdictionary:
                vdictionary[token] = 1
            if lm_dictionary[token].negative: _odata[3] += 1
            if lm_dictionary[token].positive: _odata[4] += 1
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

    _odata[15] = len(vdictionary)

    # Convert counts to %
    if _odata[2] != 0:
      for i in range(3, 9 + 1):
          _odata[i] = (_odata[i] / _odata[2]) * 100
    # Vocabulary

    return _odata

def LM_text(text):
    ''' Demonstrate the use of LM dictionary to compute metrics per file stored in
    '''

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

    for key, value in data.items():
        print(f"{key:{max_key_length}} : {value}")

    print('-'* 30)
    print('\n' * 2)

    return dict(zip(OUTPUT_FIELDS, output_data))