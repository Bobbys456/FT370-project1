import re
import pandas as pd 

with open('data\out.txt') as file: 
    text = file.read()





answers = re.findall(r'(\s+A[\s]+)([\w.,\s\'%-]+)(EndOfBlock)', text)
questions = re.findall(r'(\s+Q[\s]+)([\w.,\s\'%-]+)(EndOfBlock)', text)

dfa = pd.DataFrame(answers, columns=['type', 'text', 'ender'])
dfq = pd.DataFrame(questions, columns=['type', 'text', 'ender'])

dfa = dfa.stack().str.strip().unstack()
dfq = dfq.stack().str.strip().unstack()




dfa['count'] = dfa['text'].str.count('EndOFBlock')
print(dfa)

print(dfq)

#(?<=\s+A\s+)[\w\d]+(?=\.\.\.)'