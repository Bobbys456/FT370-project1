import re
import pandas as pd

with open('data\CORRECTED TRANSCRIPT_ Apple, Inc.(AAPL-US), Q2 2023 Earnings Call, 4-May-2023 5_00 PM ET.txt', 'r') as file: 
    text = file.read()

#create end of block to signify end of speech blocks for pattern recognition
text = re.sub(r'\.{3,}(?![\\n\\.])', 'EndOfBlock', text)
text = re.sub(r'(?<=\s{10})(\d+)(?=\n)', 'EndOfBlock', text)

#remove page end info string beacause it is not important
text = re.sub(r'1-877-FACTSET www.callstreet.com[\s\S]{0,700}\d\d\d\d', '', text)

#remove the endof block tags misplaces at the end of pages rather than at the end of speech blocks 
text = re.sub(r'\s{10,}(EndOfBlock)', '', text)



with open('data/out.txt', 'w') as file: 
    file.write(text)


with open('data/out.txt') as file: 
    text = file.read()

#\n\n(\w+\s[\w\s.]+\n)([\w\s-&/]+),([\w\s-&]+,\s[\w.]+)\s+(A\n)([\s\S]+?)(EndOfBlock)
#old regex  : (\sA\n)([\s\S]+?)(EndOfBlock)



answers = re.findall(r'\n\n(\w+\s[\w\s.]+\n)([\w\s&/-]+),([\w\s&-]+,\s[\w.]+)\s+(A\n)([\s\S]+?)(EndOfBlock)', text)
questions = re.findall(r'\n\n(\w{3,}\s[\w\s.]+\n)([\w\s&/-]+),([\w\s&-]+,\s[\w.]+)\s+(Q\n)([\s\S]+?)(EndOfBlock)', text)

dfa = pd.DataFrame(answers, columns=['name', 'title', 'comapny', 'type', 'text', 'ender'])
dfq = pd.DataFrame(questions, columns=['name', 'title', 'comapny', 'type', 'text', 'ender'])

dfa = dfa.stack().str.strip().unstack()
dfq = dfq.stack().str.strip().unstack()




dfa['count'] = dfa['text'].str.count('EndOFBlock')
print(dfa)

print(dfq)

dfq.to_excel("data/output.xlsx")

#(?<=\s+A\s+)[\w\d]+(?=\.\.\.)'