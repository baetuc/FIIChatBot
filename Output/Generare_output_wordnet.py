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
    sentences=split_into_sentences(text)
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


def get_keywords(question):
    tokenized_text = nltk.word_tokenize(question.lower())
    return [word for word in tokenized_text if word not in stopwords.words('english')]

def html_to_text(html):
    soup = BeautifulSoup(html, "lxml")
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    return(soup.get_text())
    

import google
  
def get_google_links(question,num=2):
    urls=google.search("what is the capital of Germany?")
    i = 0
    text=""
    for url in urls:
        if i < num:
            text=text+google.get_page(url)
            i+=1
        else:
            break
    return (text)

    
def get_google_response(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text.encode('UTF-8')
    return (html_to_text(content))

def get_google_summary(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text.encode('UTF-8')
    summary=re.findall('<div class="_tXc">.*<[/]div>',content)
    if len(summary) is not 0:
        return (html_to_text(summary[0]))
    else:
        return(None)
        
def get_google_answer(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text.encode('UTF-8')
    #print(content)
        
    answer=re.findall('<div class="_XWk">.*?<[/]div>',content)       #E.g. What is the president of India
    answer2=re.findall('<div class="_Tfc _j0k">.*?<[/]div>',content) #How fast is a cheetah?

    if len(answer) > 0:
        if len(answer2) > 0:
            return (html_to_text(answer[0])+' '+html_to_text(answer2[0]))
        return (html_to_text(answer[0]))
    
    answer=re.findall('<span class="_m3b".*?<[/]span>',content)  #calculator
    if len(answer) > 0:
        return (html_to_text(answer[0]))    
        
    answer=re.findall('<div class="kltat">.*?<[/]div>',content)       #what is the longest river in the world
    answer2=re.findall('<div class="ellip klmeta">.*?<[/]div>',content)

    if len(answer) > 0:
        if len(answer2) > 0:
            return (html_to_text(answer[0])+' '+html_to_text(answer2[0]))
        return (html_to_text(answer[0]))
        
    answer=re.findall('<span class="cwcot".*?<[/]span>',content)  #calculator
    if len(answer) > 0:
        return (html_to_text(answer[0]))
        
    answer=re.findall('<span class="nobr"><h2 class="r".*?<[/]span>',content)  #calculator
    if len(answer) > 0:
        return (html_to_text(answer[0]))
    return None
    
def get_google_citeations(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text.encode('UTF-8')
    cites=re.findall('<cite>.*?<[/]cite>',content)
    urls =[]
    for cite in cites:
        urls.append(html_to_text(cite))
    return urls
            
def answer_question(question):
    text=get_google_answer(question)
    if text==None:
        text=get_google_summary(question)
    if text==None:
        text=get_google_links(question)
    keywords=get_keywords(question)
    return(generate_output(text.encode('UTF-8'),keywords))
    
def generate_question(topic):
    return ("Can you think of any questions I can ask you?")


from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import httplib,socket, urllib
import simplejson
def get_sentiment(text):
    """params = urllib.urlencode({'text': text})
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    conn = httplib.HTTPConnection("http://text-processing.com:80")
    conn.request("POST", "/api/sentiment/", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
     data = response.read()
    conn.close()"""
    params = urllib.urlencode({'text': text})
    f = urllib.urlopen("http://text-processing.com/api/sentiment/", params)
    data = f.read()
    return data

#data = get_sentiment("this was a great night")
"""data = dict(data)
print(data)"""



class myHandler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    # Handler for the GET requests

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        # Send the html message
        self.wfile.write("Hello World !")
        return

    def do_POST(self):
        self._set_headers()
        print "in post method"
        self.data_string = self.rfile.read(int(self.headers['Content-Length']))
        self.send_response(200)
        self.end_headers()

        data = simplejson.loads(self.data_string)
        text=data["text"]
        keywords=data["keywords"]
        message=dict()
        message['message']=generate_output(text,keywords)
        # proceseaza datele
        pass

        try:
            s2.send(message)
        except socket.error:
            print "Failed to send data."
        return
# decomenteaza pt server
'''

PORT_NUMBER = 8080

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect(("127.0.0.1", 2222))

try:
    # Create a web server and define the handler to manage the
    # incoming request
    server = HTTPServer(('', PORT_NUMBER), myHandler)
    print 'Started httpserver on port ', PORT_NUMBER

    # Wait forever for incoming htto requests
    server.serve_forever()

except KeyboardInterrupt:
    print '^C received, shutting down the web server'
    server.socket.close()
''' 


def get_sentiment(text):
    """params = urllib.urlencode({'text': text})
    headers = {"Content-type": "application/x-www-form-urlencoded",
                "Accept": "text/plain"}
    conn = httplib.HTTPConnection("http://text-processing.com:80")
    conn.request("POST", "/api/sentiment/", params, headers)
    response = conn.getresponse()
    print response.status, response.reason
     data = response.read()
    conn.close()"""
    params = urllib.urlencode({'text': text})
    f = urllib.urlopen("http://text-processing.com/api/sentiment/", params)
    data = f.read()
    return data

#data = get_sentiment("this was a great night")
"""data = dict(data)
print(data)"""



    

import pyexcel_xls
from random import randrange
def get_questions(question_xlsx):
    data = pyexcel_xls.get_data(question_xlsx)
    #https://www.reddit.com/r/trivia/comments/3wzpvt/free_database_of_50000_trivia_questions/
    number_of_sheets = len(data)
    name_of_sheets = []
    for i in data:
        name_of_sheets.append(i)
    number_of_questions = list()
    for i in range(number_of_sheets):
        number_of_questions.append(len(data[name_of_sheets[i]]))
    #print data["3 Answers"][5][3]

def generate_question():
    sheet = randrange(0, number_of_sheets)
    question = randrange(1, number_of_questions[sheet])
    print(data[name_of_sheets[sheet]][question][0])
    return data[name_of_sheets[sheet]][question][0]

#generate_question()

# transforma din propozitie afirmativa in propozitie interogativa

question_one = 'The Knights Templar are founded to protect Christian     pilgrims in Jerusalem.'
question_two = 'Alfonso VI of Castile captures the Moorish Muslim city of Toledo, Spain.'

def modify(inputStr):

    tokens = nltk.PunktWordTokenizer().tokenize(inputStr)
    tagged = nltk.pos_tag(tokens)
    auxiliary_verbs = [i for i, w in enumerate(tagged) if w[1] == 'VBP']
    if auxiliary_verbs:
        tagged.insert(0, tagged.pop(auxiliary_verbs[0]))
    else:
        tagged.insert(0, ('did', 'VBD'))
    tagged.insert(0, ('When', 'WRB'))

    return ' '.join([t[0] for t in tagged])
    
start= time.time()
print(answer_question("what the capital of france"))
print(str(time.time()-start)+" seconds")
