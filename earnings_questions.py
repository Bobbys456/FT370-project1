def getQAs(company):
    import re
    import pandas as pd

    with open('data\\'+ company +'.txt', 'r') as file: 
        text = file.read()

    #create end of block to signify end of speech blocks for pattern recognition
    text = re.sub(r'\.{4,}(?![\\n\\.])', 'EndOfBlock\n\n\n\n', text)
    text = re.sub(r'(?<=\s{10})(\d+)(?=\n)', 'EndOfBlock\n\n\n', text)

    #remove page end info string beacause it is not important
    text = re.sub(r'1-877-FACTSET www.callstreet.com[\s\S]{0,700}\d\d\d\d', '', text)

    #remove the endof block tags misplaces at the end of pages rather than at the end of speech blocks 
    text = re.sub(r'\s{10,}(EndOfBlock)', '', text)

    #Removes everything that isnt questions and answers
    text = re.sub(r'[\s\S]+QUESTION AND ANSWER SECTION', '\n\n\n\n\n\n', text)

    #remove occurences of ...
    text = re.sub(r'\.\.\.', '', text)




    with open('data/out.txt', 'w') as file: 
        file.write(text)


    with open('data/out.txt') as file: 
        text = file.read()

    #\n\n(\w+\s[\w\s.]+\n)([\w\s-&/]+),([\w\s-&]+,\s[\w.]+)\s+(A\n)([\s\S]+?)(EndOfBlock)
    #old regex  : (\sA\n)([\s\S]+?)(EndOfBlock)

    #this one works perfect for netfilx at least, but not apple because they dont have the ,inc. after job titles in the apple one
    #\n\n(\w{3,}\s[\w\s.]+\n)([\w\s&/-]+),([\w\s&-]+,\s[\w.]+)\s+(Q\n)([\s\S]+?)(EndOfBlock)

    #this one for apple works maybe not netfilx: \n\n([A-Z]\w{2,}\s[\w\s.]+\n)([\w\s&/-]+),([\w\s&,.-]+)\s+(Q\n)([\s\S]+?)(EndOfBlock) this one has glitches in the netfix one now 



    answers = re.findall(r'\n([\w \.]+)\n([\w, \.&-]+)(A)\n([\s\S]+?)EndOfBlock', text)
    questions = re.findall(r'\n([\w \.]+)\n([\w, \.&-]+)(Q)\n([\s\S]+?)EndOfBlock', text)

    dfa = pd.DataFrame(answers, columns=['person', 'title', 'type', 'text'])
    dfq = pd.DataFrame(questions, columns=['person', 'title', 'type', 'text'])

    dfa = dfa.stack().str.strip().unstack()
    dfq = dfq.stack().str.strip().unstack()





    print(dfa)
    print(dfq)

    dfq.to_excel("data/output.xlsx")

    return dfq, dfa
