"""
Modul creat de Andrei Iacob grupa 3A5

Modulul se ocupă de parsare răspuns, căutarea propoziției potrivite, înlocuire cu sinonime și generare typo-uri.
Funcița generate_output primește un string denumit "text" și o listă de stringuri denumită "keywords" in formă lematizată bazat pe wordnet (forma această poate fi generata prin functia lemmatize), apoi returnează un string.
"""

# encoding: utf-8
from pattern.en import conjugate,pluralize
import time, requests, random, re
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from PyDictionary import PyDictionary
from bs4 import BeautifulSoup



caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"

def split_into_sentences(text):
    text = " " + text + "  "
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

validChars = {'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
              'p','q','r','s','t','u','v','w','x','y','z'}
keyboard = [['q','w','e','r','t','y','u','i','o','p'],
            ['a','s','d','f','g','h','j','k','l',';',],
            ['z','x','c','v','b','n','m',',','.','/']]

def typo(text):
    i = random.randrange(len(text))
    rand = random.random()
    if rand<0.1:
        return text[0:i]+text[i]+text[i:] #repeat character
    elif rand<0.3:
        return text[0:i]+text[i+1:]       #delete character
    elif rand<0.5:
        if i<(len(text)-1):               #switch 2 characters
            return text[0:i-1]+text[i+1]+text[i]+text[i+2:]
        else:
            return text[0:i-2]+text[i]+text[i-1]+text[i+1:]
    else:
        for j in range(len(keyboard)):   #replace character with character in close proximity
            if text[i] in keyboard[j]:
                j2=keyboard[j].index(text[i])
                if rand<0.55 and j >0:
                    j-=1
                elif rand<0.7 and j<9:
                    j+=1
                elif rand<0.85 and j2>0:
                    j2-=1
                elif j2<9:
                    j2+=1
                else:
                    j2-=1
                return text[0:i]+keyboard[j][j2]+text[i+1:]  
    
def penn_to_wn(tag):
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    elif tag.startswith('V'):
        return wn.VERB
    return None
    
def find_conjugation(verb):
    modes=['inf','1sg','1sgp','2sg','2sgp','3sg','3sgp','pl','ppl','part','ppart']
    for mode in modes:
       if conjugate(verb, mode) == verb:
           return mode
           
def match_conjugation(verb,verb_to_conjugate):  
    return conjugate(verb_to_conjugate,find_conjugation(verb))
           

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
    

def replace_with_synonyms(sentence):
    tokenized_text = nltk.word_tokenize(sentence)
    tags=nltk.pos_tag(tokenized_text)
    lemmatzr = WordNetLemmatizer()
    for i in range(len(tags)):
        token=tags[i]
        if(token[1] =="NNP" or token[1] =="VMB"):
            continue
        wn_tag = penn_to_wn(token[1])
        if not wn_tag or token[0].startswith("'"):
            continue
        if random.random()<0:
            continue
        lemma = lemmatzr.lemmatize(token[0], pos=wn_tag)
        meaning = (wn.synsets(lemma, pos=wn_tag))[0]
        n=len(meaning.lemma_names())
        if n>1:
            rand=random.randrange(1,n)
            word = meaning.lemma_names()[rand]
            if token[1].startswith('V'):
                word = match_conjugation(token[0],word)
            elif token[1].startswith('N'):
                if pluralize(token[0]) == token[0]:
                    word= pluralize(word)         
            tokenized_text[i]=word.replace('_',' ')
    return untokenize(tokenized_text)
  

def replace_with_synonyms2(sentence):
    tokenized_text = nltk.word_tokenize(sentence)
    tags=nltk.pos_tag(tokenized_text)
    dictionary=PyDictionary()
    for i in range(len(tokenized_text)):
        word=tokenized_text[i]
        wn_tag = penn_to_wn(tags[i][1])
        if not wn_tag:
            continue
        if word.startswith("'"):
            continue
        if random.random()<0.6:
            continue
        synonyms=dictionary.synonym(word)
        rand=random.randrange(0,len(synonyms))
        tokenized_text[i]=synonyms[rand]
    return untokenize(tokenized_text)
    
def get_hyponyms_synsets(synset):
    hyponyms = set()
    for hyponym in synset.hyponyms():
        hyponyms |= set(get_hyponyms_synsets(hyponym))
    return hyponyms | set(synset.hyponyms())

def get_hyponyms_names(synset):
    hyponyms = set()
    for hyponym in synset.hyponyms():
        hyponyms |= set(get_hyponyms_names(hyponym))
    lemmas = []
    for hyponym in synset.hyponyms():
        for word in hyponym.lemma_names():
            lemmas.append(word)
    return hyponyms | set(lemmas)
    
def get_hyponyms(word,tag=None):
    lemmatzr = WordNetLemmatizer()
    lemma = lemmatzr.lemmatize(word.lower(),pos=tag)
    hyponyms = set()
    for synset in wn.synsets(lemma,pos=tag):
        hyponyms |=get_hyponyms_names(synset)
    return hyponyms

def get_hypernyms_synsets(synset):
    hypernyms = set()
    for hyponym in synset.hypernyms():
        hypernyms |= set(get_hypernyms_synsets(hyponym))
    return hypernyms | set(synset.hypernyms())
    
def get_hypernyms_names(synset):
    hypernyms = set()
    for hyponym in synset.hypernyms():
        hypernyms |= set(get_hypernyms_names(hyponym))
    lemmas = []
    for hyponym in synset.hypernyms():
        for word in hyponym.lemma_names():
            lemmas.append(word)
    return hypernyms | set(lemmas)
    
def get_hypernyms(word,tag=None):
    lemmatzr = WordNetLemmatizer()
    lemma = lemmatzr.lemmatize(word.lower(),pos=tag)
    hypernyms = set()
    for synset in wn.synsets(lemma,pos=tag):
        hypernyms |=get_hypernyms_names(synset)
    return hypernyms
        
def lemmatize(words):
    lemmatzr = WordNetLemmatizer()
    lemmas = [lemmatzr.lemmatize(word.lower()) for word in words]
    return lemmas

def generate_output(text,keywords):
    sentences=split_into_sentences(text+'.')
    lemmatzr = WordNetLemmatizer()
    for sentence in sentences:
        tokenized_text = nltk.word_tokenize(sentence)
        tags=nltk.pos_tag(tokenized_text)
        words_found=[False]*len(keywords)
        words_found_count=0
        for token in tags:
            wn_tag = penn_to_wn(token[1])
            if not wn_tag:
                continue
            txt = token[0].lower().replace("’s","")
            lemma = lemmatzr.lemmatize(txt, pos=wn_tag)
            if lemma in keywords:
                        index=keywords.index(lemma)
                        if words_found[index] is False:
                            words_found_count+=1
                            words_found[index]=True
                            if words_found_count==len(keywords):
                                sentence= replace_with_synonyms(sentence)
                                while random.random()<0.1:
                                    sentence= typo(sentence)
                                return sentence
            else:
                for meaning in wn.synsets(lemma, pos=wn_tag):
                    for word in meaning.lemma_names():
                        if word in keywords:
                            index=keywords.index(word)
                            if words_found[index] is False:
                                words_found_count+=1
                                words_found[index]=True
                                if words_found_count==len(keywords):
                                    sentence= replace_with_synonyms(sentence)
                                    while random.random()<0.1:
                                        sentence= typo(sentence)
                                    return sentence
    text=replace_with_synonyms(text)
    while random.random()<0.1:
        text= typo(text)
    return text
