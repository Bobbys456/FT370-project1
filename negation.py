import spacy
import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import csv
import glob
import re
import string
import sys
from spacy.tokens import Doc
import datetime as dt
import MOD_Load_MasterDictionary_v2022 as LM
from gunfog import calculate_gunning_fog
nlp = spacy.load('en_core_web_lg')

#for testing needs to be deleted after
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
                 '# of numbers', 'avg # of syllables per word', 'average word length', 'vocabulary', 'num to words']

lm_dictionary = LM.load_masterdictionary(MASTER_DICTIONARY_FILE, print_flag=True)
#lm_dictionary, _md_header, _sentiment_categories, _sentiment_dictionaries, _stopwords, _total_documents = load_masterdictionary(MASTER_DICTIONARY_FILE, print_flag=True, get_other  =True)
#print( lm_dictionary, _md_header, _sentiment_categories, _sentiment_dictionaries, _stopwords, _total_documents )



#run python -m spacy download en_core_web_lg
def main(): 
    doc = 'I love go to the movies in boston MA a lot. I do not like movies that have a lot of blood in them because it is so red and the camera moves a lot.'
    doc = doc.upper()  # for this parse caps aren't informative so shift
    tokens = re.findall('\w+', doc)

    print(tokens)
    for index, token in enumerate(tokens):

       print(token, find_negated_wordSentIdxs_in_sent(Doc(nlp.vocab, words=tokens[index-2:index+3]), idxs_of_interest=[2]))
       """
        if not token.isdigit() and len(token) > 1 and token in lm_dictionary:
  
            if lm_dictionary[token].negative: 
                print(token + ' is negatigve \n')
            if lm_dictionary[token].positive:
                find_negated_wordSentIdxs_in_sent(str(tokens[index-10:index+10]), idxs_of_interest=10)
                print(token + ' is positive \n')
            print(lm_dictionary[token].negative)

"""
def word_is_negated(word):
    """ """

    for child in word.children:
        if child.dep_ == 'neg':
            return True

    for ancestor in word.ancestors:
        for child2 in ancestor.children:
                if child2.dep_ == 'neg':
                    return True

    return False

def find_negated_wordSentIdxs_in_sent(sent, idxs_of_interest=None):
    """ """

    for word_sent_idx, word in enumerate(sent):
        if idxs_of_interest:
            if word_sent_idx not in idxs_of_interest:
                continue
        if word_is_negated(word):
           return True
        return False



main()