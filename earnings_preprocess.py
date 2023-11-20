def getQAs(company, storedata):
    import re
    import pandas as pd

    with open('data\\'+ company +'.txt', 'r') as file: 
        text = file.read()

    text = re.sub(r'\[indiscernible\]', '', text)

    #create end of block to signify end of speech blocks for pattern recognition
    text = re.sub(r'\.{4,}(?![\\n\\.])', 'EndOfBlock\n\n\n\n', text)
    text = re.sub(r'(?<=\s{10})(\d+)(?=\n)', 'EndOfBlock\n\n\n', text)

    #remove page end info string beacause it is not important
    text = re.sub(r'1-877-FACTSET www.callstreet.com[\s\S]{0,700}\d\d\d\d', '', text)

    #remove the endof block tags misplaces at the end of pages rather than at the end of speech blocks 
    text = re.sub(r'\s{10,}(EndOfBlock)', '', text)

    #takes the prepared remarks
    prepared = re.findall(r'[\s\S]+QUESTION AND ANSWER SECTION', text)
    prepared = re.sub(r'[\s\S]+MANAGEMENT DISCUSSION SECTION[\s\S]+?EndOfBlock','', prepared[0])
    prepared = re.sub(r'QUESTION AND ANSWER SECTION','EndOfBlock', prepared)
    
    if storedata: 
        with open('data/pre.txt', 'w') as file: 
            file.write(prepared)


    #Removes the prepared remarks
    text = re.sub(r'[\s\S]+QUESTION AND ANSWER SECTION', '\n\n\n\n\n\n', text)

    #remove occurences of ...
    text = re.sub(r'\.\.\.', '', text)



    if storedata: 
        with open('data/out.txt', 'w') as file: 
            file.write(text)

    #\n\n(\w+\s[\w\s.]+\n)([\w\s-&/]+),([\w\s-&]+,\s[\w.]+)\s+(A\n)([\s\S]+?)(EndOfBlock)
    #old regex  : (\sA\n)([\s\S]+?)(EndOfBlock)

    #this one works perfect for netfilx at least, but not apple because they dont have the ,inc. after job titles in the apple one
    #\n\n(\w{3,}\s[\w\s.]+\n)([\w\s&/-]+),([\w\s&-]+,\s[\w.]+)\s+(Q\n)([\s\S]+?)(EndOfBlock)

    #this one for apple works maybe not netfilx: \n\n([A-Z]\w{2,}\s[\w\s.]+\n)([\w\s&/-]+),([\w\s&,.-]+)\s+(Q\n)([\s\S]+?)(EndOfBlock) this one has glitches in the netfix one now 


    prepared_remarks = re.findall(r'\n([\w \.-]+)\n([\w, \.&-]+)\n([\s\S]+?)EndOfBlock', prepared)
    answers = re.findall(r'\n([\w \.-]+)\n([\w, \.&-]+)(A)\n([\s\S]+?)EndOfBlock', text)
    questions = re.findall(r'\n([\w \.-]+)\n([\w, \.&-]+)(Q)\n([\s\S]+?)EndOfBlock', text)

    dfa = pd.DataFrame(answers, columns=['person', 'title', 'type', 'text'])
    dfq = pd.DataFrame(questions, columns=['person', 'title', 'type', 'text'])
    dfp = pd.DataFrame(prepared_remarks, columns=['person', 'title', 'text'])

    dfa = dfa.stack().str.strip().unstack()
    dfq = dfq.stack().str.strip().unstack()
    dfp = dfp.stack().str.strip().unstack()

    print(dfa)
    print(dfq)
    print(dfp)

    
    dfq.to_csv("data/"+ company + "questions.csv")
    dfa.to_csv("data/"+ company + "answers.csv")
    dfp.to_csv("data/"+ company + "prepared_remarks.csv")

    
    return dfq, dfa, dfp
