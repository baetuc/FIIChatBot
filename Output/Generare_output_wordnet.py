# encoding: utf-8
from pattern.en import conjugate,pluralize
import time, requests, random, re
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from PyDictionary import PyDictionary
from bs4 import BeautifulSoup
from unidecode import unidecode

lemmatzr = WordNetLemmatizer()


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
keyboard = [['1','2','3','4','5','6','7','8','9','0','-'],
            ['q','w','e','r','t','y','u','i','o','p',';'],
            ['a','s','d','f','g','h','j','k','l',';',"'"],
            ['z','x','c','v','b','n','m',',','.','/','?']]

def typo(text):
    try:
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
                    elif rand<0.7 and j<3:
                        j+=1
                    elif rand<0.85 and j2>0:
                        j2-=1
                    elif j2<9:
                        j2+=1
                    else:
                        j2-=1
                    return text[0:i]+keyboard[j][j2]+text[i+1:]  
    except Exception:
        return text
        
    
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
  

def replace_with_synonyms(sentence,prob=0.4):
    try:
        tokenized_text = nltk.word_tokenize(sentence)
        tags=nltk.pos_tag(tokenized_text)
        for i in range(len(tags)):
            token=tags[i]
            if(token[1] =="NNP" or token[1] =="VMB"):
                continue
            wn_tag = penn_to_wn(token[1])
            if not wn_tag or token[0].startswith("'"):
                continue
            if random.random()>prob:
                continue
            try:
                lemma = lemmatzr.lemmatize(token[0], pos=wn_tag)
                meanings = (wn.synsets(lemma, pos=wn_tag))
                if len(meanings)>0:
                    meaning=meanings[0]
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
            except Exception:
                pass
        return untokenize(tokenized_text)
    except Exception:
        return sentence  

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
    if tag != None:
        lemma = lemmatzr.lemmatize(word.lower(),pos=tag)
    else:
        lemma = lemmatzr.lemmatize(word.lower())
    hypernyms = set()
    for synset in wn.synsets(lemma,pos=tag):
        hypernyms |=get_hypernyms_names(synset)
    return hypernyms
        
    
    
    
import phonenumbers
import datefinder
common_codes = ['RO','GB','US','RU','FR','CN','JP','DE','CA']
def is_phone_number(number):
    if number[0]!='+':
        try: 
            numobj = phonenumbers.parse('+'+number,None)
            if phonenumbers.is_valid_number(numobj):
                return True
        except Exception:
            pass
        for code in common_codes:
            try:
                numobj = phonenumbers.parse(number,code)
                if phonenumbers.is_valid_number(numobj):
                    return True
            except Exception:
                pass            
        return False
    else:
        try: 
            numobj = phonenumbers.parse(number,None)
            if phonenumbers.is_valid_number(numobj):
                return True
        except Exception:
            return False
            
    
aproximation_words=['about ',"'round ",'around ','approximately ',"I think it's ","last I checked it was ","I would guess about ","Not sure, around ","last I checked it was approximately ","","","",""]
    
def number_round(number,round_to=4,no_decimals=True):
    if len(number)<=round_to:
        return number
    if number.count('.')>0:
        
        try:
            num = round(float(number.replace(',','')),round_to-number.replace(',','').index('.'))
            
            if num % 1 == 0 or no_decimals:
                    num = int(num)
            
        except Exception:
            print number
            return number
        return aproximation_words[random.randint(0,len(aproximation_words)-1)] +str(num)
    try:
        num = int(number.replace(',',''))
        
    except Exception:
            print number
            return number
    return (aproximation_words[random.randint(0,len(aproximation_words)-1)] + str(int(round(num,round_to-len(number.replace(',',''))))))
    
def number_error(number):
    try:
        num = float(number)
    except:
        print number
        return number
    zeros = 10
    while (num % zeros) == 0:
        zeros*=10
    zeros/=10
    return str(((int(num*0.01))*random.randint(0,4))*zeros+num)

    
def round_numbers(text):
    if '=' in text:
        return text
    tokenized_text = nltk.word_tokenize(text)
    tags=nltk.pos_tag(tokenized_text)
    i=0
    print tags
    while i<len(tags):
        token=tags[i]
        
        if token[1]=='CD' and token[0][0]!='0':
                
                start_i = i
                number = token[0]
                while(i<(len(tags)-1) and tags[i+1][1]=='CD'):
                    not_number = re.match("[a-z/]",tags[i+1][0])
                    if not_number!=None:
                        break
                    number+=tags[i+1][0]
                    i+=1
                not_number = re.match("[a-z/]",number.lower())
                if (not is_phone_number(number)) and number.count('.')<2 and not_number==None and len(number)>3:
                    number=number_round(number)
                    for j in range(start_i,i):
                        del tags[start_i]
                        del tokenized_text[start_i]
                    tags[start_i]=(number,'CD')
                    tokenized_text[start_i]=number
                    token=tags[start_i]
                    i = start_i
                else:
                    token=(number,'CD')
        i+=1
    return untokenize(tokenized_text)
    
year_phrases=['in the ']
def date_round(text,round_years=True):
    matches = datefinder.find_dates(text,source=True,index=True)
    offset = 0
    offset2=0
    for match in matches:
        offset+=offset2
        offset=0
        tokenized_text = nltk.word_tokenize(match[1])
        tags=nltk.pos_tag(tokenized_text)
        i = 0
        while i<(len(tags)):
            if tags[i][1]=='CD':
                is_not_number=re.match('[^0-9]',tags[i][0])
                if is_not_number==None:
                    if len(tags[i][0])<3 and i<(len(tags)-1) and ((tags[i+1][1]=='NNP') or (i>0 and tags[i+1][1]=='CD' and tags[i-1][1]=='NNP')):
                        
                        if round_years:
                            if i<(len(tags)-2) and (tags[i+1][1]=='NNP' and tags[i+2][1]=='CD') and len(tags[i+2][0])>2:
                                i+=2
                                if random.random()<0.5 and len(tags[i][0])==4:
                                    tokenized_text[i]="'"+tokenized_text[i][2:]
                                    offset2+=1
                                if random.random()<0.7 and tags[i][0][len(tags[i][0])-1]!=0  and tags[i][0][:2]!='20':
                                    tokenized_text[i]=tokenized_text[i][:len(tokenized_text[i])-1]+'0s'
                                    offset2-=1
                                    if tokenized_text[i][0]=="'":
                                        tokenized_text[i]=" "+tokenized_text[i][1:]
                                    if random.random()<0.5:
                                        tokenized_text[i]='in the '+tokenized_text[i]
                                        offset2-=6
                                i-=2
                            elif i<(len(tags)-1) and (tags[i-1][1]=='NNP' and tags[i+1][1]=='CD') and len(tags[i+1][0])>2:
                                i+=1
                                if random.random()<0.5 and len(tags[i][0])==4:
                                    tokenized_text[i]="'"+tokenized_text[i][2:]
                                    offset2+=0
                                if random.random()<0.7 and tags[i][0][len(tags[i][0])-1]!=0 and tags[i][0][:2]!='20':
                                    tokenized_text[i]=tokenized_text[i][:len(tokenized_text[i])-1]+'0s'
                                    offset2-=1
                                    if tokenized_text[i][0]=="'":
                                        tokenized_text[i][0]=' '
                                        
                                    if random.random()<0.5:
                                        tokenized_text[i]='in the '+tokenized_text[i]
                                        offset2-=6
                                i-=1
                        offset2 += len(tags[i][0])
                        del tags[i]
                        del tokenized_text[i]
            i+=1
        
        if match[2][0]==0:
            if (match[2][1]-offset-1)<len(text):
                text= untokenize(tokenized_text)+' '+text[match[2][1]-offset-1:]
            else:
                text = untokenize(tokenized_text)
        else:
            if (match[2][1]-offset-1)<len(text):
                text=text[0:match[2][0]-offset]+' '+untokenize(tokenized_text)+' '+text[match[2][1]-offset:]
            else:
                text=text[0:match[2][0]-offset]+' '+untokenize(tokenized_text)
    return text

def number_and_date_round(text):
    matches = datefinder.find_dates(text,source=True,index=True)
    offset = 0
    offset2=0
    scan_for_numbers_start=0
    for match in matches:
        length = len(text)
        text = text[0:scan_for_numbers_start]+round_numbers(text[scan_for_numbers_start:match[2][0]-offset])+text[match[2][0]-offset:]
        offset+=offset2+(length - len(text))
        offset2=0
        tokenized_text = nltk.word_tokenize(match[1])
        tags=nltk.pos_tag(tokenized_text)
        i = 0
        while i<(len(tags)):
            if tags[i][1]=='CD':
                if len(tags[i][0])<3 and (tags[i+1][1]=='NNP' or (tags[i+1][1]=='CD' and tags[i+1][1]=='NNP')):
                    offset2 += len(tags[i][0])
                    del tags[i]
                    del tokenized_text[i]
            i+=1
        
        if match[2][0]==0:
            if (match[2][1]-offset-1)<len(text):
                text= untokenize(tokenized_text)+' '+text[match[2][1]-offset-1:]
            else:
                text = untokenize(tokenized_text)
        else:
            if (match[2][1]-offset-1)<len(text):
                text=text[0:match[2][0]-offset]+' '+untokenize(tokenized_text)+' '+text[match[2][1]-offset:]
            else:
                text=text[0:match[2][0]-offset]+' '+untokenize(tokenized_text)
        scan_for_numbers_start=match[2][1]-offset
    text = text[0:scan_for_numbers_start]+round_numbers(text[scan_for_numbers_start:])
    return text
    
def number_error2(number):
    trailing_zeros = 0
    i = len(number)-1
    while number[i]=='0' or number[i]=='.' or number[i]==',':
        trailing_zeros+=1
        i+=1
    
    if (len(number)-trailing_zeros)<4:
        return number
    if '.' in number:
        if (len(number)-number.index('.'))<(len(number)-4):
            del number[number.index('.'):len(number)]
        else:
            del number[4:len(number)]
            if number[3]=='.':
                del number[3]
                
        trailing_zeros = 0
        i = len(number)-1
        while number[i]=='0' or number[i]=='.' or number[i]==',':
            trailing_zeros+=1
            i+=1
        if (len(number)-trailing_zeros)<4:
            return number
    for i in range(4,len(number)):
        number[i]='0'
    return aproximation_words[random.randint(0,len(aproximation_words)-1)] + number

    
    
def lemmatize(words):
    lemmas = [lemmatzr.lemmatize(word.lower()) for word in words]
    return lemmas
  
def generate_output(text,keywords):
    sentences=split_into_sentences(text+'.')
    for sentence in sentences:
        tokenized_text = nltk.word_tokenize(sentence)
        tags=nltk.pos_tag(tokenized_text)
        words_found=[False]*len(keywords)
        words_found_count=0
        for token in tags:
            wn_tag = penn_to_wn(token[1])

            txt = token[0].lower().replace("’s","")
            try:
                if not wn_tag:
                    lemma = lemmatzr.lemmatize(txt)
                else:
                    lemma = lemmatzr.lemmatize(txt, pos=wn_tag)
                ok = True
            except Exception:
                lemma =txt
                ok = False
                
            
            if lemma in keywords:
                        index=keywords.index(lemma)
                        if words_found[index] is False:
                            words_found_count+=1
                            words_found[index]=True
                            if words_found_count==len(keywords):
                                sentence=date_round(sentence)
                                sentence= round_numbers(sentence)
                                sentence= replace_with_synonyms(sentence)
                                while random.random()<0.1:
                                    sentence= typo(sentence)
                                return sentence
            elif ok:
                for meaning in wn.synsets(lemma, pos=wn_tag):
                    for word in meaning.lemma_names():
                        if word in keywords:
                            index=keywords.index(word)
                            if words_found[index] is False:
                                words_found_count+=1
                                words_found[index]=True
                                if words_found_count==len(keywords):
                                    sentence=date_round(sentence)
                                    sentence= round_numbers(sentence)
                                    sentence= replace_with_synonyms(sentence)
                                    while random.random()<0.1:
                                        sentence= typo(sentence)
                                    return sentence
    text=date_round(text)
    text= round_numbers(text)
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
    content = r.text
    print(content)
    return (html_to_text(content))


def get_google_summary(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text
    summary=re.findall('<div class="_tXc">.*<[/]div>',content)
    if len(summary) is not 0:
        return (html_to_text(summary[0]))
    summary=re.findall('<ol class="_l0g">.*?<[/]ol>',content)
    if len(summary) is not 0:
        return (html_to_text(summary[0]))
    summary=re.findall('<div class="_sPg">.*?<[/]div>',content)
    if len(summary) is not 0:
        return (html_to_text(summary[0]))
    summary=re.findall('<div class="_o0d">.*<[/]div>',content)
    if len(summary) is not 0:
        return (html_to_text(summary[0]))
    summary=re.findall('[(noun)(adverb)(verb)(adjective)]<[/]div><ol.*?<[/]li',content)
    response = ""
    for i in range(len(summary)):    
        response+=' ' +summary[i]
    if len(summary) is not 0:
        return (html_to_text(response)[1:])
    return(None)
        
def get_google_answer(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text
    #print(content)
        
    answer=re.findall('<div class="_XWk">.*?<[/]div>',content)       #E.g. Who is the president of India
    answer2=re.findall('<div class="_Tfc _j0k">.*?<[/]div>',content) #How fast is a cheetah?

    if len(answer) > 0:
        if len(answer2) > 0:
            return (html_to_text(answer[0])+' '+html_to_text(answer2[0]))
        return (html_to_text(answer[0]))
    
    answer=re.findall('<span class="_m3b".*?<[/]span>',content)  #calculator
    if len(answer) > 0:
        answers=""
        for ans in answer:
            answers+=html_to_text(ans)
        return answers 
    
    answer=re.findall('<div class="kltat">.*?<[/]div>',content)       #what is the longest river in the world
    answer2=re.findall('<div class="ellip klmeta">.*?<[/]div>',content)
    
    if len(answer) > 0:
        if len(answer2) > 0:
            return (html_to_text(answer[0])+' '+html_to_text(answer2[0]))
        return (html_to_text(answer[0]))
        
    answer=re.findall('<span class="cwcot".*?<[/]span>',content)  
    
    if len(answer) > 0:
        return (html_to_text(answer[0]))
        
    answer=re.findall('<span class="nobr"><h2 class="r".*?<[/]span>',content)  
    if len(answer) > 0:
        return (html_to_text(answer[0]))
        
    answer=re.findall('<span class="_G0d">.*?<[/]span>',content)  
    if len(answer) > 0:
        answers=""
        for ans in answer:
            answers+=html_to_text(ans)
        return answers
        
    answer=re.findall('<td style="font-size:16px">.*?<[/]td>',content)  
    if len(answer) > 0:
        return (html_to_text(answer[0]))
    
    return None

def get_google_answer2(question):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    # header variable
    headers = { 'User-Agent' : user_agent }
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url,headers=headers)
    content = r.text
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
    
def get_google_correction(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text.encode('UTF-8')
    print content
    correction=re.findall('<a class="spell".*?<[/]a>',content)
    if len(correction)>0:
        return html_to_text(correction[0])
    return None

def get_google_questions(question):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    # header variable
    headers = { 'User-Agent' : user_agent }
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url,headers=headers)
    content = r.text.encode('UTF-8')
    questions=re.findall('<div class="_rhf">.*?<[/]div>',content)
    return [(html_to_text(q)) for q in questions]
    
def get_google_citeations(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text
    cites=re.findall('<cite>.*?<[/]cite>',content)
    urls =[]
    for cite in cites:
        text = html_to_text(cite)
        if text.startswith('https://') or text.startswith('www.'):
            urls.append(text)
    return urls
            

    
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
    

#print(replace_with_synonyms("Paris 8766, France's 5th capital, is a major European city and a global center for art, fashion, gastronomy and culture."))
#print(answer_question("WHAT IS 2+2?"))

'''
lt=[]
for synset in wn.synsets('cat'):
    lt.append(synset)
    for hypernym in synset.hypernyms():
        lt.append(hypernym)
print(lt)
'''

class topic:
    def __init__(self,decay=0.9,synset_decay=0.5,hypernym_decay=0.8,max_level = None):
        self.used_synsets=[]
        self.scores=[]   
        self.decay=decay
        self.synset_decay=synset_decay
        self.hypernym_decay=hypernym_decay
        self.max_level =max_level
    def get_topic(self):
        return self.used_synsets[self.scores.index(max(self.scores))].lemma_names()[0]
    def process_keywords(self,keywords,importance=1,decay=True):
        if decay:
            self.scores=[score*self.decay for score in self.scores]
        for word in keywords:
           it=1.0
           for synset in wn.synsets(word):
               if synset in self.used_synsets:
                   self.scores[self.used_synsets.index(synset)]+=importance*(it)
               else:
                   self.used_synsets.append(synset)
                   self.scores.append(importance*(it))
               it=it*self.synset_decay
               hypernyms = synset.hypernyms()
               if len(hypernyms)>0:
                   self.process_synsets(hypernyms,0,importance*it)
            
    def process_synsets(self,synsets,level,importance,decay=False,):
        if decay:
            self.scores=[score*self.decay for score in self.scores]   
        it=1.0
        for synset in synsets:
               if synset in self.used_synsets:
                   self.scores[self.used_synsets.index(synset)]+=importance*(it)
               else:
                   self.used_synsets.append(synset)
                   self.scores.append(importance*(it))
               it=it*self.hypernym_decay
               if (self.max_level != None):
                   if level > self.max_level:
                       continue
               hypernyms = synset.hypernyms()
               if len(hypernyms)>0:
                   self.process_synsets(hypernyms,level+1,importance=importance*it)
            
tpc = topic()
tpc.process_keywords(['cat','bird','pig'])
tpc.process_keywords(['dog','mouse','bat'])
wrds = [x for x in [y for y in get_hypernyms('cat') if y in get_hypernyms('bird')] if x in get_hypernyms('pig')]
#print(tpc.get_topic())

yes_verbs = ['is','are','am','was','were','will','would','should','can', 'could','do','did']

def yes_no(sentence):
    tokenized_text = nltk.word_tokenize(sentence)
    tags=nltk.pos_tag(tokenized_text)
    token=tags[0]
    txt = token[0].lower().replace("’s","")
    try:
        lemma = lemmatzr.lemmatize(txt)
        if lemma == None or (tags[1][0]!='you' and (tags[2][0]!='tell' or tags[2][0]!='inform') and tags[3][0]!='me'):
            return None
        if lemma in yes_verbs:
            if random.random()>0.5:
                answer = 'yes'
            else:
                answer = 'no'
            return answer
    except Exception:
        return None
   
        
class FavoriteHandler:
    def __init__(self):
        """
        Clasa care se ocupa cu intrebari de tipul "What is your favorite X"
        """
        self._given_answers = {}
        self._given_reasons = {}
        self._domains = {
            "color" : ["blue", "red", "orange", "cyan", "black"],
            "food" : ["pizza", "hamburger", "salad", "sushi", "soup"],
            "car" : ["Ford", "Mercedes", "Ferrari", "Dacia", "BMW", "Honda"],
            "song" : ["You make me wanna", "We are Young", "Rainbow in the Dark", "Stayin Alive"],
            "band|artist" : ["Iron Maiden", "Eminem", "The Beatles", "ABBA"],
            "drink" : ["Water", "Beer", "Wine", "Vodka!"],
            "book" : ["The Lord of The Rings", "The Da Vinci Code", "Harry Potter", "50 Shades of Grey"],
            "movie" : ["Inception", "Django Unchained", "Seven Samurai", "Argo"],
            "TV show" : ["Breaking Bad", "Game of Thrones", "Doctor Who", "South Park"],
            "actor" : ["Tom Hanks", "Danny de Vito", "Robert de Niro", "Keanu Reeves"],
            "actress" : ["Scarlett Johansson", "Cate Blanchett", "Jennifer Lawrence", "Natalie Portman"],
            "site" : ["Google", "Youtube", "Facebook", "Reddit"],
            "activity|leisure" : ["Hiking", "Surfing the web", "Playing video games"],
            "animal|pet" : ["Cat", "Dog", "Turtle", "Bird"],
            "brand|company" : ["Coca Cola", "Apple", "Microsoft", "Nestle"],
            "country" : ["Romania", "Germany", "United States of America", "Japan"],
            "school subject" : ["Artificial Intelligence", "Mathematics", "English"],
            "language" : ["English", "Romanian", "German", "Japaneese"],
            "sport" : ["Football", "Baseball", "Running", "Boxing"],
            "team" : ["Manchester United", "Real Madrid", "NY Yankers"],
            "holiday" : ["Christmas", "New Year", "Easter"],
            "number" : ["1","3","7","9","13"],
            "soda" : ["Cocal Cola", "7Up", "Mountain Dew"],
            "video game|computer game" : ["Counter Strike", "Overwatch", "Half Life"],
            "author|writer|poet" : ["Edgar Allan Poe", "J.R.R. Tolkien","J.K. Rowling"]
        }
        self._reasons = {
            "color" : {
                "blue" : ["It reminds me of the sky", "I think it's a calming color. I even painted my room that color!", "It reminds me of a little baby boy"],
                "red" : ["I think it's a really powerful color", "It reminds me of the sunset", "I think it gives me energy!"],
                "orange" : ["It reminds me of a summer sunset", "I really like the fruit with the same name I guess", "I think i look well in orange."],
                "cyan" : ["It's a special color", "Not too many people think of cyan as their favorite color!", "It looks brilliant"],
                "black" : ["I find it oddly soothing", "It makes me sleepy", "I think it's an elegant color"]
            },
            "food" : {
                "pizza" : ["It's yummy!", "It's nice to eat at parties", "You can order it and eat without needing to leave home or cook"],
                "hamburger" : ["I really like beef", "It's preety quick to cook", "I know a really nice burger joint"],
                "salad" : ["I doesn't make you fat", "I think it's very fresh", "It doesn't need any meat to be good"],
                "sushi" : ["It's a lean food", "I really like fish", "I think it's exotic"],
                "soup" : ["It also hydrate you", "I really like vegetabl soup", "You can just throw anything into boiling water and you're done"]
            },
            "car" : {
                "Ford" : ["They are really cheap and good", "They have both average-Joe cars, and things like the Mustang", "I really like how the gears change"],
                "Mercedes" : ["I think they are really luxurious", "I think they are really well build", "I think the rear-wheel drive it's a big plus"],
                "Ferrari" : ["I like fast cars","Why wouldn't I? ","I allways wanted a Ferrari"],
                "Dacia" : ["I like romanian cars","I think it is affordable and suited for our roads"],
                "BMW" : ["I like fast and good looking cars","It represents the perfect harmony between elegance, comfort and dynamism"],
                "Honda" : ["They have a low fuel consumption and a lot a systems","I like Asian cars"],
            },
            "song" : {
                "You make me wanna" : ["I got married to this song", "It gives me energy"],
                "We are young" : ["I have a young spirit and this song describes me (wink)", "It is a song full of energy"],
                "Rainbow in the Dark" : ["This is my rock side", "I think it is the best rock/heavy metal voice ever"],
                "Stayin alive" :["This would be the first song on my mixtape for a zombie apocalypse", "I think it is a great funeral song (joke)"],
            },
            "band|artist" : {
                "Iron Maiden" : ["Who doesn't like them?!", "I really like heavy metal"],
                "Eminem" : ["I like his style", "I like the lyrics"],
                "The Beatles" : ["I like good music", "Probably the best band of all time"],
                "ABBA" : ["The best music was from the good old days","I sing their songs in the shower, every word"],
            },
            "drink" : {
                "Water" :["It keeps me alive!", "I can'y live without it"],
                "Beer" :["Beer it's just Beer, what is not to love about it?", "I like the taste"],
                "Wine" :["I like the taste", "It helps you travel the World in a bottle"],
                "Vodka" :["Nothing like a good old bottle of Rubinoff or Zelcos.", "It helps me reset my memory"],
            },
            "book" : {
                "The Lord of The Rings" : ["I like the story", "I like the characters", "I really like how the places are described"],
                "The Da Vinci Code" : ["I like how it chalanges religion", "I really like the main character", "I like how Dan Brown writes"], 
                "Harry Potter": ["I loved the book when I was a kid", "I like both the book and the movie", "I love the author"], 
                "50 Shades of Grey" : ["You don't want to know", "I hope I'll find a Mr. Grey some day", "It's a spicy book"],
            },
            "soda" : {
            	"Coca Cola" : ["I prefer to drink it instead of coffee", "I like the pretty bottle", "It's nice to cool off in the summer"],
            	"7Up" : ["It's better than Sprite", "I like that it's not that sweet", "It's really bubbly"],
            	"Mountain Dew" : ["It's yellow", "It's better than Coke", "It has a really nice taste"]
            },
            "video game|computer game" : {
            	"Counter Strike" : ["It's a game that is still good after all these years", "Everyone who likes games has played CS at least once", "I love how a mod came so far"],
            	"Overwatch" : ["It combines the MOBA and FPS genres", "The characters are really balanced", "I like to play with my team"],
            	"Half Life" : ["I think it revolutionized the genre", "It had really good graphics for it's age", "I like the story"]
            },
            "author|writer|poet" : {
            	"Edgar Allan Poe" : ["I like poetry", "I really like 'The Raven'", "I really like his symbolism"],
            	"J.R.R. Tolkien" : ["I really like The Hobbit!", "I love The Lord of the Rings", "I like how he created a huge world by writing"],
            	"J.K. Rowling" : ["I grew up with Harry Potter", "I really like her style of writing", "Everyone loves Harry Potter!"]
            }
        }
    
    def _get_known_domain(self, question):
        for domain in self._domains:
            r = ".*(" + domain + ").*"
            if re.match(r, question, re.IGNORECASE):
                return domain
        return None
    
    def _get_unknown_domain(self, question):
        r = ".*what.*favorite ([a-zA-Z]+).*"
        m = re.match(r,question,re.IGNORECASE)
        if m and m.group(1):
            return m.group(1)
        return None

    def is_favorite_question(self, question):
        if "what" in question.lower() and "favorite" in question.lower():
            return True
        return False

    def _get_answer_from_domain(self, domain):
        if self._given_answers.get(domain):
            return "I already told you my favorite is %s"%(self._given_answers.get(domain))
        else:
            response = random.choice(self._domains.get(domain))
            self._given_answers[domain] = response
            real_domain = domain
            if "|" in domain:
                real_domain = domain.split("|")[0]
            return "My favorite %s is %s"%(real_domain, response)

    def answer_what(self, question):
        if not self.is_favorite_question(question):
            return "Honestly, I don't know what to say"
        domain = self._get_known_domain(question)
        if domain:
            answer = self._get_answer_from_domain(domain)
            return answer
        else:
            domain = self._get_unknown_domain(question)
            if domain:
                return "I don't think I have a favorite %s"%(domain)
            else:
                return "Honestly, I don't know what to say"

    def is_why_question(self, question):
        if "why" in question.lower() and "favorite" in question.lower():
            return True
        return False
    
    def _get_query_from_what_question(self, question):
        r = ".*why.*is ([a-zA-Z]+).* your favorite.*"
        m = re.match(r, question, re.IGNORECASE)
        if m and m.group(1):
            return m.group(1)
        return None

    def answer_why(self, question):
        if not self.is_why_question(question):
            return "Honestly, I don't know what to say"
        query = self._get_query_from_what_question(question)
        if query:
            answer_given = False
            for domain in self._domains:
                if self._given_answers.get(domain) == query:
                    answer_given = True
                    break

            if not answer_given:
                return "I didn't say that was my favorite!"

            given_reason = self._given_reasons.get(query)
            if given_reason:
                return "I already told you that!"
            given_reason = random.choice(self._reasons.get(domain).get(query))
            self._given_reasons[query] = given_reason
            return given_reason
        return "I don't really have a favorite"
        

fh = FavoriteHandler()
past_questions = []
repeat_phrases = ["I already told you. ","You asked that before. ","As I told you before. ","I'm repeating myself here. ","Just like I told you. ","" ]
def answer_question(question):
    for q in past_questions:
        if q[0] == question:
            r = random.randint(0,len(repeat_phrases)-1)
            return (repeat_phrases[r]+replace_with_synonyms(q[1]))
    text = None
    if fh.is_favorite_question(question):
        text = fh.answer_what(question)
    if fh.is_why_question(question):
        text = fh.answer_why(question)
    if text==None:
        text=get_google_answer(question)
    if text==None:
        text=get_google_summary(question)
    if text==None:
        text=yes_no(question)
    if text==None:
        text=get_google_links(question)
    keywords=get_keywords(unidecode(question))
    answer = generate_output(unidecode(text.encode('UTF-8')),keywords)
    past_questions.append((question,answer))
    return answer
    
start= time.time()
print(answer_question("How do you make goulash?"))
print(str(time.time()-start)+" seconds")
