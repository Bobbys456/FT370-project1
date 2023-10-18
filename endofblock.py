import re

with open('data\CORRECTED TRANSCRIPT_ Netflix, Inc.(NFLX-US), Q2 2023 Earnings Call, 19-July-2023 6_00 PM ET (1).txt', 'r') as file: 
    text = file.read()

text = re.sub(r'\.{3,}(?![\\n\\.])', 'EndOfBlock', text)

with open('data/out.txt', 'w') as file: 
    file.write(text)