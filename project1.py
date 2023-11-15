import re
import numpy as np
import re
import nltk
from nltk.corpus import cmudict
from sklearn.metrics.pairwise import cosine_similarity
from matplotlib import pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.metrics import jaccard_score
import editdistance
from earnings_analyses import analyze_call

#this file creates multiple similarity measures between the last two 10ks for the comapnies Moderna and tesla.
#more documentation follows in the file named earnings_analyses.py 

#the html files generated in the main directory are a visulaiztion of the document differences openable in browser

nltk.download('stopwords')
stopwords = nltk.corpus.stopwords.words('english')

with open('project1_data/TSLA-Basic-annual-filing-for-period-end-31Dec21-07-Feb-22.txt', 'r', encoding='utf-8') as f:
    pagetext = f.read()

with open('project1_data\TSLA-Basic-annual-filing-for-period-end-31Dec22-31-Jan-23.txt', 'r', encoding='utf-8') as f:
    pagetext2 = f.read()

with open('project1_data\MRNA-Basic-annual-filing-for-period-end-31Dec21-25-Feb-22.txt', 'r', encoding='utf-8') as f:
    pagetext3 = f.read()

with open('project1_data\MRNA-Basic-annual-filing-for-period-end-31Dec22-24-Feb-23.txt', 'r', encoding='utf-8') as f:
    pagetext4 = f.read()

pagetext = pagetext.split(r'ITEM 7.            MANAGEMENTS DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS')[-1]
tsla_22_mda = pagetext.split(r'ITEM 8.      FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA')[0].lower()

pagetext2 = pagetext2.split(r'ITEM 7.            MANAGEMENTS DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS')[-1]
tsla_23_mda = pagetext2.split(r'ITEM 8.       FINANCIAL STATEMENTS AND SUPPLEMENTARY DATA')[0].lower()

pagetext3 = pagetext3.split(r'Item 7. MANAGEMENTS DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS')[-1]
mrna_22_mda = pagetext3.split(r'Item 8. Financial Statements and Supplementary Data')[0].lower()

pagetext4 = pagetext4.split(r'Item 7. MANAGEMENTS DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS')[-1]
mrna_23_mda = pagetext4.split(r'Item 8. Financial Statements and Supplementary Data')[0].lower()




def parse_raw_text(text):
    
    """removing newlines (github copilot)"""
    text = text.replace('\n', ' ')

    """removing 10-k"""
    text = text.replace('10-k', '')
    
    """removing numbers (github copilot)"""
    text = re.sub(r'\d+', '', text) 

    """replace covid- with covid"""
    text = text.replace('covid-', 'covid')

    """removing unnecessary commas"""
    text = text.replace(' ,', ',')
    text = text.replace(',,', ',')

    """formatting text to remove bullet points"""    
    text = text.replace(f'•', '')

    """removing % (github copilot)"""
    text = text.replace('%', '')

    """remove 's from words"""
    text = text.replace("'s", 's')

    """remove $ from words"""
    text = text.replace('$', '')

    """removing spaces before periods"""
    text = text.replace(' .', '.')

    """replacing ., with ,"""
    text = text.replace(',.', ',')

    """replacing . million with million"""
    text = text.replace('. million', ' million')

    """replace u.s with us, if it is not in the end of the sentence (chatgpt)"""
    text = re.sub(r'[u][.][s][.](?=\s+\w)', 'us', text)

    """removing (), (,) and (.)"""
    text = text.replace('()', '')
    text = text.replace('(,)', '')
    text = text.replace('(.)', '')

    """removing _"""
    text = text.replace('_', '')

    """removing , , , """
    text = text.replace(', , , ', '')

    """remove long spaces (chatgpt)"""
    text = re.sub(r' +', ' ', text)

    """replace million and billion periods with million or billion"""
    text = text.replace('. million', ' million')
    text = text.replace('. billion', ' billion')

    return text


"""function to fit and transform the count vectorizer"""
def count_vectorize_pair(text_1, text_2, remove_stopwords):
    vectorizer = CountVectorizer(stop_words=remove_stopwords)
    vectorizer.fit([text_1+text_2])
    vectorized_text_1 = vectorizer.transform([text_1])
    vectorized_text_2 = vectorizer.transform([text_2])
    return vectorized_text_1, vectorized_text_2

"""function to vectorize text using TFIDF"""
def tfidf_vectorizer(text_1, text_2, remove_stopwords):
    vectorizer = TfidfVectorizer(stop_words=remove_stopwords)
    vectorizer.fit([text_1+text_2])
    vectorized_text_1 = vectorizer.transform([text_1])
    vectorized_text_2 = vectorizer.transform([text_2])
    return vectorized_text_1, vectorized_text_2

"""function to create metrics"""
def create_metrics(list1, list2, title, stopwords):
    cosine_similarity_value = cosine_similarity(list1, list2)
    jaccard_similarity_value = jaccard_score(np.sign(list1[0]), np.sign(list2[0]))
    print(f'{title} {stopwords} metrics')
    print(f'cosine similarity: {cosine_similarity_value}')
    print(f'jaccard similarity: {jaccard_similarity_value}')
    print(f'edit distance: {editdistance.eval(list1[0], list2[0])}, edit distance normalized: {editdistance.eval(list1[0], list2[0])/len(list1[0])}')
    print(75*'-')

"""fnction to find cosine similarity between two texts"""
def run_cosine_similarity(text_pair, title):
    text1 = text_pair[0]
    text2 = text_pair[1]
    
    """used github copilot for autocompletion"""
    text1_vectorized_stopwords, text2_vectorized_stopwords = count_vectorize_pair(text1, text2, None)
    text1_vectorized_no_stopwords, text2_vectorized_no_stopwords = count_vectorize_pair(text1, text2, stopwords)

    text1_tfidf_stopwords, text2_tfidf_stopwords = tfidf_vectorizer(text1, text2, None)
    text1_tfidf_no_stopwords, text2_tfidf_no_stopwords = tfidf_vectorizer(text1, text2, stopwords)

    text1_vectorized_stopwords, text2_vectorized_stopwords = text1_vectorized_stopwords.toarray(), text2_vectorized_stopwords.toarray()
    text1_vectorized_no_stopwords, text2_vectorized_no_stopwords = text1_vectorized_no_stopwords.toarray(), text2_vectorized_no_stopwords.toarray()

    text1_tfidf_stopwords, text2_tfidf_stopwords = text1_tfidf_stopwords.toarray(), text2_tfidf_stopwords.toarray()
    text1_tfidf_no_stopwords, text2_tfidf_no_stopwords = text1_tfidf_no_stopwords.toarray(), text2_tfidf_no_stopwords.toarray()

    """creating and displaying metrics"""
    create_metrics(text1_vectorized_stopwords, text2_vectorized_stopwords, title, 'stopwords')
    create_metrics(text1_vectorized_no_stopwords, text2_vectorized_no_stopwords, title, 'no stopwords')
    create_metrics(text1_tfidf_stopwords, text2_tfidf_stopwords, title, 'tfidf stopwords')
    create_metrics(text1_tfidf_no_stopwords, text2_tfidf_no_stopwords, title, 'tfidf no stopwords')

    return text1, text2

"""function to create sentences from text"""
def create_sentences(text):
    return re.findall(r'\b[a-z][^.!?]*[.!?]', text)

"""used chatgpt for the html formatting"""
def write_html(sentences0, sentences1, title0, title1):
    with open(f"{title0.strip(' 2021')}_output.html", "w", encoding="utf-8") as file:
        file.write("<!DOCTYPE html>\n")
        file.write("<html lang='en'>\n")
        file.write("<head>\n")
        file.write("<meta charset='UTF-8'>\n")
        file.write("<meta http-equiv='X-UA-Compatible' content='IE=edge'>\n")
        file.write("<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
        file.write(f"<title>{title0} and {title1} Sentences</title>\n")
        file.write("</head>\n")
        file.write("<body>\n")
        
        file.write("<div style='float: left; width: 50%;'>\n")
        for sentence in sentences0:
            if sentence in sentences1:
                file.write(f"<p style='color: green;'>{sentence}<br>\n</p>")
            else:
                file.write(f"<p style='color: red;'>{sentence}<br>\n</p>")
        file.write("</div>\n")

        file.write("<div style='float: right; width: 50%;'>\n")
        for sentence in sentences1:
            if sentence in sentences0:
                file.write(f"<p style='color: green;'>{sentence}<br>\n</p>")
            else:
                file.write(f"<p style='color: red;'>{sentence}<br>\n</p>")
    
        file.write("</div>\n")
        file.write("</body>\n")
        file.write("</html>\n")
        file.close()


def most_similar_sentence(target_sentence, sentences_list):
    """Return the most similar sentence from sentences_list to the target_sentence."""
    max_shared_words = 0
    most_similar = None
    for sentence in sentences_list:
        shared_words = sum(1 for word in target_sentence.split() if word in sentence.split())
        if shared_words > max_shared_words:
            max_shared_words = shared_words
            most_similar = sentence
    return most_similar

def write_only_changes_html(sentences0, sentences1, title0, title1):
    with open(f"{title0.strip(' 2021')}_only_changes_output.html", "w", encoding="utf-8") as file:
        file.write("<!DOCTYPE html>\n")
        file.write("<html lang='en'>\n")
        file.write("<head>\n")
        file.write("<meta charset='UTF-8'>\n")
        file.write("<meta http-equiv='X-UA-Compatible' content='IE=edge'>\n")
        file.write("<meta name='viewport' content='width=device-width, initial-scale=1.0'>\n")
        file.write(f"<title>{title0} and {title1} Sentences</title>\n")
        file.write("</head>\n")
        file.write("<body>\n")

        for sentence in sentences0:
            corresponding_sentence = most_similar_sentence(sentence, sentences1)

            # Sentence from sentences0
            file.write("<div style='float: left; width: 48%; padding: 10px; word-wrap: break-word; vertical-align: top;'>\n")
            for word in sentence.split(' '):
                if corresponding_sentence and word in corresponding_sentence.split(' '):
                    file.write(f"<span style='color: green;'>{word} </span>")
                else:
                    file.write(f"<span style='color: red;'>{word} </span>")
            file.write("</div>\n")

            # Corresponding most similar sentence from sentences1
            file.write("<div style='float: right; width: 48%; padding: 10px; word-wrap: break-word; vertical-align: top;'>\n")
            if corresponding_sentence:
                for word in corresponding_sentence.split(' '):
                    if word in sentence.split(' '):
                        file.write(f"<span style='color: green;'>{word} </span>")
                    else:
                        file.write(f"<span style='color: red;'>{word} </span>")
            file.write("</div>\n")

            # Clear floats after each pair of sentences to ensure proper alignment
            file.write("<div style='clear: both;'></div>\n")
            #file.write("<br><br>\n")  # Added extra breaks for more space between sentence pairs

        file.write("</body>\n")
        file.write("</html>\n")



if __name__ == "__main__":
    text_list = [tsla_22_mda, tsla_23_mda, mrna_22_mda, mrna_23_mda]

    text_list = [parse_raw_text(text) for text in text_list]

    tsla_list = text_list[:2]
    mrna_list = text_list[2:]
    
    run_cosine_similarity(tsla_list, "TSLA")
    run_cosine_similarity(mrna_list, "MRNA")

    tsla_2021_sentences = create_sentences(tsla_list[0])
    tsla_2022_sentences = create_sentences(tsla_list[1])

    mrna_2021_sentences = create_sentences(mrna_list[0])
    mrna_2022_sentences = create_sentences(mrna_list[1])

    write_html(tsla_2021_sentences, tsla_2022_sentences, "TSLA 2021", "TSLA 2022")
    write_html(mrna_2021_sentences, mrna_2022_sentences, "MRNA 2021", "MRNA 2022")

    write_only_changes_html(tsla_2021_sentences, tsla_2022_sentences, "TSLA 2021", "TSLA 2022")
    write_only_changes_html(mrna_2021_sentences, mrna_2022_sentences, "MRNA 2021", "MRNA 2022")

    analyze_call('tesla')
    analyze_call('mrna')


    