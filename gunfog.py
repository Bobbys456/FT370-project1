
import re
import nltk
from nltk.corpus import cmudict

# Load the CMU Pronouncing Dictionary
nltk.download('cmudict')
cmud = cmudict.dict()

def count_syllables(word):
    """Count the number of syllables in a word."""
    if word.lower() not in cmud:
        #print("MISSING WORD",word)
        return 0
    return max([len([y for y in x if y[-1].isdigit()]) for x in cmud[word.lower()]])


def count_syllables_corpus(corpus):
    """Count the number of syllables in a corpus."""
    total_syllables = 0
    total_words = 0
    for word in corpus.split():
        syllables = count_syllables(word)
        total_syllables += syllables
        total_words += 1
    return total_syllables, total_words

def calculate_gunning_fog(corpus):
    # Count the number of sentences
    sentence_count = len(re.findall(r'\b[A-Z][^.!?]*[.!?]', corpus))

    # Count the number of words
    word_count = len(re.findall(r'\b\w+\b', corpus))

    # Estimate the number of complex words (words with 3 or more syllables)
    complex_word_count = 0
    for word in re.findall(r'\b\w+\b', corpus):
        syllable_count = count_syllables(word)
        if syllable_count >= 3:
            complex_word_count += 1

    # TB - to avoid a division by 0 error
    if sentence_count == 0:
      sentence_count = 1

    # Calculate the average sentence length (words per sentence)
    average_sentence_length = word_count / sentence_count

    # Calculate the percentage of complex words in the text
    complex_word_percentage = (complex_word_count / word_count) * 100

    # Calculate the Gunning Fog Index
    fog_index = 0.4 * (average_sentence_length + complex_word_percentage)

    return fog_index

