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
                       properties={"annotators":"tokenize,ssplit,pos,parse,natlog,openie",
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