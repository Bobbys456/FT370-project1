import re
import pandas as pd

with open('data/CORRECTED TRANSCRIPT_ Netflix, Inc.(NFLX-US), Q2 2023 Earnings Call, 19-July-2023 6_00 PM ET (1).txt', 'r') as file: 
    text = file.read()

text = re.sub(r'\.{3,}(?![\\n\\.])', 'EndOfBlock', text)
text = re.sub(r'(?<=\s{10})(\d+)(?=\n)', 'EndOfBlock', text)


with open('data/out.txt', 'w') as file: 
    file.write(text)


with open('data/out.txt') as file: 
    text = file.read()

#(\w+\s[\w\.]+\s\w+\n)([\w-\s&]+, [\w-\s&]+,[\w-\s&]+)([\S\s]+\sA\n)([\s\S]+)(?!EndOfBlock)



answers = re.findall(r'(\sA\n)([\s\S]+?)(EndOfBlock)', text)
questions = re.findall(r'(\sQ\n)([\s\S]+?)(EndOfBlock)', text)

dfa = pd.DataFrame(answers, columns=['type', 'text', 'ender'])
dfq = pd.DataFrame(questions, columns=['type', 'text', 'ender'])

dfa = dfa.stack().str.strip().unstack()
dfq = dfq.stack().str.strip().unstack()




dfa['count'] = dfa['text'].str.count('EndOFBlock')
print(dfa)

print(dfq)

#(?<=\s+A\s+)[\w\d]+(?=\.\.\.)'