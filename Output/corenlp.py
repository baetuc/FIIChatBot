'''
Modul creat de Iacob Andrei-Constantin grupa 3A5
Modulul se ocupă cu parseare coreNLP și obținerea împărțirea frazelor în propoziții.
 
install:
    py -2 -m pip install wget
    wget http://nlp.stanford.edu/software/stanford-corenlp-full-2016-10-31.zip
    unzip stanford-corenlp-full-2016-10-31.zip

    source:    http://stackoverflow.com/questions/32879532/stanford-nlp-for-python
    
start server cmd:
    cd corenlp-python\stanford-corenlp-full-2016-10-31
    java -mx5g -cp "*" edu.stanford.nlp.pipeline.StanfordCoreNLPServer
'''

from pycorenlp import StanfordCoreNLP
import nltk 



def get_res(sentence):
    nlp = StanfordCoreNLP('http://localhost:9000')
    res = nlp.annotate(sentence,
                       properties={"annotators":"tokenize,ssplit,pos,parse,natlog,openie,coref",
                                    "outputFormat": "json"
                                    })
    return (res)

import re

split = '[(]CC .*?[)]'
split2 = '(SBAR .*?)'
remove = ['(ADJP', '(-ADV',  '(ADVP',  '(-BNF',  '(CC',  '(CD',  '(-CLF',  '(-CLR',  '(CONJP',  '(-DIR',  '(DT',  '(-DTV',  '(EX',  '(-EXT',  '(FRAG',  '(FW',  '(-HLN',  '(IN',  '(INTJ',  '(JJ',  '(JJR',  '(JJS',  '(-LGS',  '(-LOC',  '(LS',  '(LST',  '(MD',  '(-MNR',  '(NAC',  '(NN',  '(NNS',  '(NNP',  '(NNPS',  '(-NOM',  '(NP',  '(NX',  '(PDT',  '(POS',  '(PP',  '(-PRD',  '(PRN',  '(PRP',  '(-PRP',  '(PRP$','(PRP-S',  '(PRT',  '(-PUT',  '(QP',  '(RB',  '(RBR',  '(RBS',  '(RP',  '(RRC', '(ROOT',  '(S',  '(SBAR',  '(SBARQ',  '(-SBJ',  '(SINV',  '(SQ',  '(SYM',  '(-TMP',  '(TO',  '(-TPC',  '(-TTL',  '(UCP',  '(UH',  '(VB',  '(VBD',  '(VBG',  '(VBN',  '(VBP',  '(VBZ',  '(-VOC',  '(VP',  '(WDT',  '(WHADJP',  '(WHADVP',  '(WHNP',  '(WHPP',  '(WP',  '(WP$',  '(WP-S',  '(WRB',  '(X','(.',  ')', '\n','\r']
remove.sort(reverse=True)
                                                                                                                                                                                                                   
def get_clauses(s):
    clauses=[]
    for sen in re.split(split,s['parse']):
        for sen2 in re.split(split2,sen):
                print(sen2)
                print('\n')
                for rmv in remove:
                    sen4=sen2.replace(rmv,"")
                    sen2=sen4
                clauses.append(sen2)
    return (clauses)


def get_clauses2(s):
    clauses = []
    for clause in s['openie']:
        clauses.append(clause['subject']+' '+clause['relation']+' '+clause['object'])
    return (clauses)

sentence = "My dog also likes eating sausage but my mother doesn't."
res = get_res(sentence)
 

for s in res["sentences"]:
    print(s['parse'])
    print(s.keys())
    print(s['openie'])
    for dep in s['enhancedDependencies']:
        print(dep)
print(get_clauses(s))    

def replace_with_coreference(res,text):
    sentences = split_into_sentences(text)
    tokeniezd_text=[]
    tags = []
    for sentence in sentences:
        tokenized_sentence = nltk.word_tokenize(sentence)
        tokeniezd_text.append(tokenized_sentence)
        tags.append(nltk.pos_tag(tokenized_sentence))
    for s in res["corefs"]:
        print(res["corefs"][s])  
        corefs = res["corefs"][s]
        i=0
        while i<len(corefs):
            if tags[corefs[i]['sentNum']-1][corefs[i]['startIndex']-1][1]== 'NNP': 
                i+=1
            else:
                for j in range(i-1,-1,-1):
                    if tags[corefs[j]['sentNum']-1][corefs[j]['startIndex']-1][1]== 'NNP': 
                        if corefs[j]['gender']==corefs[i]['gender'] and corefs[j]['animacy']==corefs[i]['animacy'] and corefs[j]['number']==corefs[i]['number']:
                            tokeniezd_text[corefs[i]['sentNum']-1][corefs[i]['startIndex']-1]=corefs[j]['text']
                            for j in range(corefs[i]['startIndex'],corefs[i]['endIndex']-1):
                                del tokeniezd_text[corefs[i]['sentNum']-1][j]
                            break
    
                i+=1
        result = ""
        for sentence in tokeniezd_text:
            if(sentence[0]!='.'):
                result+=(untokenize(sentence))
        return result
            
def replace_with_coreference2(res,text):
    sentences = split_into_sentences(text)
    tokeniezd_text=[]
    for sentence in sentences:
        tokeniezd_text.append(nltk.word_tokenize(sentence))
    for s in res["corefs"]:
        print(res["corefs"][s])  
        corefs = res["corefs"][s]
        i=0
        while i<len(corefs):
            if corefs[i]['isRepresentativeMention'] == True: 
                i+=1
            else:
                for j in range(i-1,-1,-1):
                    if corefs[j]['isRepresentativeMention'] == True: 
                        if corefs[j]['gender']==corefs[i]['gender'] and corefs[j]['animacy']==corefs[i]['animacy'] and corefs[j]['number']==corefs[i]['number']:
                            tokeniezd_text[corefs[i]['sentNum']-1][corefs[i]['startIndex']-1]=corefs[j]['text']
                            for j in range(corefs[i]['startIndex'],corefs[i]['endIndex']-1):
                                del tokeniezd_text[corefs[i]['sentNum']-1][j]
                            break
    
                i+=1
        result = ""
        for sentence in tokeniezd_text:
            if(sentence[0]!='.'):
                result+=(untokenize(sentence))
        return result

 caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
    
def split_into_sentences(text):
    text = " " + text + ".  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(caps + "[.]" + caps + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + caps + "[.]"," \\1<prd>",text)
    if '"' in text: text = text.replace('."','".')
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences
    
def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .',  '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
         "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()

#text = "Barack Obama was born in Hawaii.  He is the president. Obama was elected in 2008."
text = "Barack Obama was born in Hawaii. He's the president. Donald Trump won 2016 election. He is made of chocolate."
res = get_res(text)


        

print(replace_with_coreference(res,text))
