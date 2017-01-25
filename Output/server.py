# encoding: utf-8
import cheer_up, avoid_personal
from pattern.en import conjugate, pluralize
import subprocess
from bottle import run, post, request, response, get, route
import json
import nltk
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from unidecode import unidecode
import re
import random
import urllib
import urllib2
import time
import phonenumbers
import datefinder


def generate_question(cuvant):
    url = 'http://answerthepublic.com/seeds'

    hdr = {

        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ro-RO,ro;q=0.8,en-US;q=0.6,en;q=0.4',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'answerthepublic.com',
        'Origin': 'http://answerthepublic.com',
        'Referer': 'http://answerthepublic.com/',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'Cookie': '_google_suggest_session=OENEWm9SUlVzaEt3OXZmWnZVNVgrL0dqOVZmanpJS3I3b1hDL21pMHp5T0pZeEl1RlVUdzhFb3hpK1kxaEFhUUMwWSs3dHNDNjRONkpzSjdEVnZ5cS82bHlVK04wZWNPdXA0ZlBkb3lFMUdmZEJlTUtNRWUrQTJ3b3k5WE9aYkk4bzRraXZVbFdjZzhyYlBoRUxyV2hiSCtQK0dEWEhBSEloQ01lV3FnbldYZURGU0NLZFN4OEg0UndVc2p3Y0hBT3NYM2ttSGcrdSttakpseno4US9HN1NjRlhic2grQitnK1I3V2NLdS9WaWQ0NitWYmo1cDd2aGZSd3g4aTUyVmg3enJSUS9ZNEhNQlY4Q0hGcGQxem5XOGQwN3JIRmNjeDRaKzc1ZDRJQWs9LS1mQUtZVXc4WWpWNTduT2U5RXllT2lnPT0=--b56df51a14730a303007f0b306ea5b94e03c554c; request_method=POST'
    }

    hdr2 = {

        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'ro-RO,ro;q=0.8,en-US;q=0.6,en;q=0.4',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
    }

    # Prepare the data
    values = {
        'utf8': r'%E2%9C%93',
        'authenticity_token': 'jNJDcx2WdmVhihkdDST+cPUkdqMip2MrUmB5d20YOusYcbE8PmE3gOsQfd/wKf42OsjmxDHyVQi4nzyifkocuA==',
        'seed[keyword]': cuvant,
        'seed[country]': 'UK',
        'commit': 'Get questions'
    }

    data = urllib.urlencode(values)

    # data = """utf8=%E2%9C%93&authenticity_token=jNJDcx2WdmVhihkdDST%2BcPUkdqMip2MrUmB5d20YOusYcbE8PmE3gOsQfd%2FwKf42OsjmxDHyVQi4nzyifkocuA%3D%3D&seed%5Bkeyword%5D=dresses&seed%5Bcountry%5D=UK&commit=Get+questions"""
    # print data
    # Send HTTP POST request
    req = urllib2.Request(url, data, headers=hdr)
    response = urllib2.urlopen(req)

    html = response.read()
    hdr2['Cookie'] = response.headers['Set-Cookie']

    regex = """data-seed-id=\"(.*?)\""""

    m = re.search(regex, html)
    print
    m.group(1)

    listamea = list()
    url = "http://answerthepublic.com/seeds/" + m.group(1)
    time.sleep(2)
    i = 0
    while i is 0:
        print
        i
        req = urllib2.Request(url, headers=hdr2)
        response = urllib2.urlopen(req)
        time.sleep(3)
        html = response.read()

        stop = """<h2 id="prepositions" data-magellan-destination="prepositions" class="text-center"><strong>.*?</strong> <strong id="prepositions-heading-count" class="text-cta">.*?</strong> Prepositions</h2>"""
        html = re.split(stop, html)[0]

        regex = r"""<li class="suggestion">.*?<a target="_blank" href=".*?">(.*?)</a>.*?</li>"""

        for a in re.finditer(regex, html, flags=re.DOTALL):
            i = 5
            listamea.append(a.group(1))
    # Print the result

    return random.choice(listamea)


def get_keywords(question):
    tokenized_text = nltk.word_tokenize(question.lower())
    return [word for word in tokenized_text if word not in stopwords.words('english')]


lemmatzr = WordNetLemmatizer()

caps = "([A-Z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"


def split_into_sentences(text):
    text = " " + text + "  "
    text = text.replace("\n", " ")
    text = re.sub(prefixes, "\\1<prd>", text)
    text = re.sub(websites, "<prd>\\1", text)
    if "Ph.D" in text: text = text.replace("Ph.D.", "Ph<prd>D<prd>")
    text = re.sub("\s" + caps + "[.] ", " \\1<prd> ", text)
    text = re.sub(acronyms + " " + starters, "\\1<stop> \\2", text)
    text = re.sub(caps + "[.]" + caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>\\3<prd>", text)
    text = re.sub(caps + "[.]" + caps + "[.]", "\\1<prd>\\2<prd>", text)
    text = re.sub(" " + suffixes + "[.] " + starters, " \\1<stop> \\2", text)
    text = re.sub(" " + suffixes + "[.]", " \\1<prd>", text)
    text = re.sub(" " + caps + "[.]", " \\1<prd>", text)
    if '"' in text: text = text.replace('."', '".')
    if "\"" in text: text = text.replace(".\"", "\".")
    if "!" in text: text = text.replace("!\"", "\"!")
    if "?" in text: text = text.replace("?\"", "\"?")
    text = text.replace(".", ".<stop>")
    text = text.replace("?", "?<stop>")
    text = text.replace("!", "!<stop>")
    text = text.replace("<prd>", ".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


validChars = {'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
              'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z'}
keyboard = [['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-'],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', ';'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'"],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', '?']]


def typo(text):
    try:
        i = random.randrange(len(text))
        rand = random.random()
        if rand < 0.1:
            return text[0:i] + text[i] + text[i:]  # repeat character
        elif rand < 0.3:
            return text[0:i] + text[i + 1:]  # delete character
        elif rand < 0.5:
            if i < (len(text) - 1):  # switch 2 characters
                return text[0:i - 1] + text[i + 1] + text[i] + text[i + 2:]
            else:
                return text[0:i - 2] + text[i] + text[i - 1] + text[i + 1:]
        else:
            for j in range(len(keyboard)):  # replace character with character in close proximity
                if text[i] in keyboard[j]:
                    j2 = keyboard[j].index(text[i])
                    if rand < 0.55 and j > 0:
                        j -= 1
                    elif rand < 0.7 and j < 3:
                        j += 1
                    elif rand < 0.85 and j2 > 0:
                        j2 -= 1
                    elif j2 < 9:
                        j2 += 1
                    else:
                        j2 -= 1
                    return text[0:i] + keyboard[j][j2] + text[i + 1:]
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
    modes = ['inf', '1sg', '1sgp', '2sg', '2sgp', '3sg', '3sgp', 'pl', 'ppl', 'part', 'ppart']
    for mode in modes:
        if conjugate(verb, mode) == verb:
            return mode


def match_conjugation(verb, verb_to_conjugate):
    return conjugate(verb_to_conjugate, find_conjugation(verb))


def untokenize(words):
    """
    Untokenizing a text undoes the tokenizing operation, restoring
    punctuation and spaces to the places that people expect them to be.
    Ideally, `untokenize(tokenize(text))` should be identical to `text`,
    except for line breaks.
    """
    text = ' '.join(words)
    step1 = text.replace("`` ", '"').replace(" ''", '"').replace('. . .', '...')
    step2 = step1.replace(" ( ", " (").replace(" ) ", ") ")
    step3 = re.sub(r' ([.,:;?!%]+)([ \'"`])', r"\1\2", step2)
    step4 = re.sub(r' ([.,:;?!%]+)$', r"\1", step3)
    step5 = step4.replace(" '", "'").replace(" n't", "n't").replace(
        "can not", "cannot")
    step6 = step5.replace(" ` ", " '")
    return step6.strip()


def replace_with_synonyms(sentence, prob=0.4):
    tokenized_text = nltk.word_tokenize(sentence)

    tags = nltk.pos_tag(tokenized_text)
    for i in range(len(tags)):
        if random.random() > prob:
            continue
        token = tags[i]
        if (token[1] == "NNP" or token[1] == "VMB" or token[1] == "CD" or token[1] == "NNPS"):
            continue
        wn_tag = penn_to_wn(token[1])
        if not wn_tag or token[0].startswith("'"):
            continue
        try:
            lemma = lemmatzr.lemmatize(token[0], pos=wn_tag)
            meanings = (wn.synsets(lemma, pos=wn_tag))
            if len(meanings) > 0:
                meaning = meanings[0]
                n = len(meaning.lemma_names())
                if n > 1:
                    rand = random.randrange(1, n)
                    word = meaning.lemma_names()[rand]
                    if token[1].startswith('V'):
                        word = match_conjugation(token[0], word)
                    elif token[1].startswith('N'):
                        if pluralize(token[0]) == token[0]:
                            word = pluralize(word)
                    tokenized_text[i] = word.replace('_', ' ')
        except Exception:
            pass
    try:
        return untokenize(tokenized_text)
    except Exception:
        return sentence


def replace_with_synonyms2(sentence):
    tokenized_text = nltk.word_tokenize(sentence)
    tags = nltk.pos_tag(tokenized_text)
    dictionary = PyDictionary()
    for i in range(len(tokenized_text)):
        word = tokenized_text[i]
        wn_tag = penn_to_wn(tags[i][1])
        if not wn_tag:
            continue
        if word.startswith("'"):
            continue
        if random.random() < 0.6:
            continue
        synonyms = dictionary.synonym(word)
        rand = random.randrange(0, len(synonyms))
        tokenized_text[i] = synonyms[rand]
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


def get_hyponyms(word, tag=None):
    lemma = lemmatzr.lemmatize(word.lower(), pos=tag)
    hyponyms = set()
    for synset in wn.synsets(lemma, pos=tag):
        hyponyms |= get_hyponyms_names(synset)
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


def get_hypernyms(word, tag=None):
    if tag != None:
        lemma = lemmatzr.lemmatize(word.lower(), pos=tag)
    else:
        lemma = lemmatzr.lemmatize(word.lower())
    hypernyms = set()
    for synset in wn.synsets(lemma, pos=tag):
        hypernyms |= get_hypernyms_names(synset)
    return hypernyms


def lemmatize(words):
    lemmas = [lemmatzr.lemmatize(word.lower()) for word in words]
    return lemmas


common_codes = ['RO', 'GB', 'US', 'RU', 'FR', 'CN', 'JP', 'DE', 'CA']


def is_phone_number(number):
    if number[0] != '+':
        try:
            numobj = phonenumbers.parse('+' + number, None)
            if phonenumbers.is_valid_number(numobj):
                return True
        except Exception:
            pass
        for code in common_codes:
            try:
                numobj = phonenumbers.parse(number, code)
                if phonenumbers.is_valid_number(numobj):
                    return True
            except Exception:
                pass
        return False
    else:
        try:
            numobj = phonenumbers.parse(number, None)
            if phonenumbers.is_valid_number(numobj):
                return True
        except Exception:
            return False


aproximation_words = ['about ', "'round ", 'around ', 'approximately ', "I think it's ", "last I checked it was ",
                      "I would guess about ", "Not sure, around ", "last I checked it was approximately ", "", "", "",
                      ""]


def number_round(number, round_to=4, no_decimals=True):
    if len(number) <= round_to:
        return number
    if number.count('.') > 0:

        try:
            num = round(float(number.replace(',', '')), round_to - number.replace(',', '').index('.'))

            if num % 1 == 0 or no_decimals:
                num = int(num)

        except Exception:
            print
            number
            return number
        return aproximation_words[random.randint(0, len(aproximation_words) - 1)] + str(num)
    try:
        num = int(number.replace(',', ''))

    except Exception:
        print
        number
        return number
    return (aproximation_words[random.randint(0, len(aproximation_words) - 1)] + str(
        int(round(num, round_to - len(number.replace(',', ''))))))


def number_error(number):
    try:
        num = float(number)
    except:
        print
        number
        return number
    zeros = 10
    while (num % zeros) == 0:
        zeros *= 10
    zeros /= 10
    return str(((int(num * 0.01)) * random.randint(0, 4)) * zeros + num)


def round_numbers(text):
    if '=' in text:
        return text
    tokenized_text = nltk.word_tokenize(text)
    tags = nltk.pos_tag(tokenized_text)
    i = 0
    while i < len(tags):
        token = tags[i]

        if token[1] == 'CD' and token[0][0] != '0':

            start_i = i
            number = token[0]
            while (i < (len(tags) - 1) and tags[i + 1][1] == 'CD'):
                not_number = re.match("[a-z/]", tags[i + 1][0])
                if not_number != None:
                    break
                number += tags[i + 1][0]
                i += 1
            not_number = re.match("[a-z/]", number.lower())
            if (not is_phone_number(number)) and number.count('.') < 2 and not_number == None and len(number) > 3:
                number = number_round(number)
                for j in range(start_i, i):
                    del tags[start_i]
                    del tokenized_text[start_i]
                tags[start_i] = (number, 'CD')
                tokenized_text[start_i] = number
                token = tags[start_i]
                i = start_i
            else:
                token = (number, 'CD')
        i += 1
    return untokenize(tokenized_text)


year_phrases = ['in the ']


def date_round(text, round_years=True):
    matches = datefinder.find_dates(text, source=True, index=True)
    offset = 0
    offset2 = 0
    for match in matches:
        offset += offset2
        offset = 0
        tokenized_text = nltk.word_tokenize(match[1])
        tags = nltk.pos_tag(tokenized_text)
        i = 0
        while i < (len(tags)):
            if tags[i][1] == 'CD':
                is_not_number = re.match('[^0-9]', tags[i][0])
                if is_not_number == None:
                    if len(tags[i][0]) < 3 and i < (len(tags) - 1) and (
                        (tags[i + 1][1] == 'NNP') or (i > 0 and tags[i + 1][1] == 'CD' and tags[i - 1][1] == 'NNP')):

                        if round_years:
                            if i < (len(tags) - 2) and (tags[i + 1][1] == 'NNP' and tags[i + 2][1] == 'CD') and len(
                                    tags[i + 2][0]) > 2:
                                i += 2
                                if random.random() < 0.5 and len(tags[i][0]) == 4:
                                    tokenized_text[i] = "'" + tokenized_text[i][2:]
                                    offset2 += 1
                                if random.random() < 0.7 and tags[i][0][len(tags[i][0]) - 1] != 0 and tags[i][0][
                                                                                                      :2] != '20':
                                    tokenized_text[i] = tokenized_text[i][:len(tokenized_text[i]) - 1] + '0s'
                                    offset2 -= 1
                                    if tokenized_text[i][0] == "'":
                                        tokenized_text[i] = " " + tokenized_text[i][1:]
                                    if random.random() < 0.5:
                                        tokenized_text[i] = 'in the ' + tokenized_text[i]
                                        offset2 -= 6
                                i -= 2
                            elif i < (len(tags) - 1) and (tags[i - 1][1] == 'NNP' and tags[i + 1][1] == 'CD') and len(
                                    tags[i + 1][0]) > 2:
                                i += 1
                                if random.random() < 0.5 and len(tags[i][0]) == 4:
                                    tokenized_text[i] = "'" + tokenized_text[i][2:]
                                    offset2 += 0
                                if random.random() < 0.7 and tags[i][0][len(tags[i][0]) - 1] != 0 and tags[i][0][
                                                                                                      :2] != '20':
                                    tokenized_text[i] = tokenized_text[i][:len(tokenized_text[i]) - 1] + '0s'
                                    offset2 -= 1
                                    if tokenized_text[i][0] == "'":
                                        tokenized_text[i][0] = ' '

                                    if random.random() < 0.5:
                                        tokenized_text[i] = 'in the ' + tokenized_text[i]
                                        offset2 -= 6
                                i -= 1
                        offset2 += len(tags[i][0])
                        del tags[i]
                        del tokenized_text[i]
            i += 1

        if match[2][0] == 0:
            if (match[2][1] - offset - 1) < len(text):
                text = untokenize(tokenized_text) + ' ' + text[match[2][1] - offset - 1:]
            else:
                text = untokenize(tokenized_text)
        else:
            if (match[2][1] - offset - 1) < len(text):
                text = text[0:match[2][0] - offset] + ' ' + untokenize(tokenized_text) + ' ' + text[
                                                                                               match[2][1] - offset:]
            else:
                text = text[0:match[2][0] - offset] + ' ' + untokenize(tokenized_text)
    return text


def number_and_date_round(text):
    matches = datefinder.find_dates(text, source=True, index=True)
    offset = 0
    offset2 = 0
    scan_for_numbers_start = 0
    for match in matches:
        length = len(text)
        text = text[0:scan_for_numbers_start] + round_numbers(text[scan_for_numbers_start:match[2][0] - offset]) + text[
                                                                                                                   match[
                                                                                                                       2][
                                                                                                                       0] - offset:]
        offset += offset2 + (length - len(text))
        offset2 = 0
        tokenized_text = nltk.word_tokenize(match[1])
        tags = nltk.pos_tag(tokenized_text)
        i = 0
        while i < (len(tags)):
            if tags[i][1] == 'CD':
                if len(tags[i][0]) < 3 and (
                        tags[i + 1][1] == 'NNP' or (tags[i + 1][1] == 'CD' and tags[i + 1][1] == 'NNP')):
                    offset2 += len(tags[i][0])
                    del tags[i]
                    del tokenized_text[i]
            i += 1

        if match[2][0] == 0:
            if (match[2][1] - offset - 1) < len(text):
                text = untokenize(tokenized_text) + ' ' + text[match[2][1] - offset - 1:]
            else:
                text = untokenize(tokenized_text)
        else:
            if (match[2][1] - offset - 1) < len(text):
                text = text[0:match[2][0] - offset] + ' ' + untokenize(tokenized_text) + ' ' + text[
                                                                                               match[2][1] - offset:]
            else:
                text = text[0:match[2][0] - offset] + ' ' + untokenize(tokenized_text)
        scan_for_numbers_start = match[2][1] - offset
    text = text[0:scan_for_numbers_start] + round_numbers(text[scan_for_numbers_start:])
    return text


def number_error2(number):
    trailing_zeros = 0
    i = len(number) - 1
    while number[i] == '0' or number[i] == '.' or number[i] == ',':
        trailing_zeros += 1
        i += 1

    if (len(number) - trailing_zeros) < 4:
        return number
    if '.' in number:
        if (len(number) - number.index('.')) < (len(number) - 4):
            del number[number.index('.'):len(number)]
        else:
            del number[4:len(number)]
            if number[3] == '.':
                del number[3]

        trailing_zeros = 0
        i = len(number) - 1
        while number[i] == '0' or number[i] == '.' or number[i] == ',':
            trailing_zeros += 1
            i += 1
        if (len(number) - trailing_zeros) < 4:
            return number
    for i in range(4, len(number)):
        number[i] = '0'
    return aproximation_words[random.randint(0, len(aproximation_words) - 1)] + number


def generate_output(text, q):
    if text == None:
        print 'text is none'
    keywords=get_keywords(q)
    sentences = split_into_sentences(text + '.')
    for sentence in sentences:
        tokenized_text = nltk.word_tokenize(sentence)
        tags = nltk.pos_tag(tokenized_text)
        words_found = [False] * len(keywords)
        words_found_count = 0
        i = 0

        while i < len(tags):
            token = tags[i]
            wn_tag = penn_to_wn(token[1])

            txt = token[0].lower().replace("'s", "")
            try:
                if not wn_tag:
                    lemma = lemmatzr.lemmatize(txt)
                else:
                    lemma = lemmatzr.lemmatize(txt, pos=wn_tag)
                ok = True
            except Exception:
                lemma = txt
                ok = False

            if lemma in keywords:
                index = keywords.index(lemma)
                if words_found[index] is False:
                    words_found_count += 1
                    words_found[index] = True
                    if words_found_count == len(keywords):
                        sentence = date_round(sentence)
                        sentence = round_numbers(sentence)
                        sentence = replace_with_synonyms(sentence)
                        while random.random() < 0.05:
                            sentence = typo(sentence)
                        return sentence
            elif ok:
                for meaning in wn.synsets(lemma, pos=wn_tag):
                    for word in meaning.lemma_names():
                        if word in keywords:
                            index = keywords.index(word)
                            if words_found[index] is False:
                                words_found_count += 1
                                words_found[index] = True
                                if words_found_count == len(keywords):
                                    sentence = date_round(sentence)
                                    sentence = round_numbers(sentence)
                                    sentence = replace_with_synonyms(sentence)
                                    while random.random() < 0.05:
                                        sentence = typo(sentence)
                                    return sentence
            i += 1
    text = date_round(text)
    text = round_numbers(text)
    text = replace_with_synonyms(text)
    while random.random() < 0.05:
        text = typo(text)
    return text


listaMea = r"""Is it worse to fail at something or never attempt it in the first place?
If you could choose just one thing to change about the world, what would it be?
To what extent do you shape your own destiny, and how much is down to fate?
Does nature shape our personalities more than nurture?
Should people care more about doing the right thing, or doing things right?
What one piece of advice would you offer to a newborn infant?
Where is the line between insanity and creativity?"""

def addTopic(topicText):
    if topicText and random.random()< 0.10 :
        return topicText
    return ""


def parseJson(data):
    global listaMea
    split = True
    ret_text = None

    topicText = data['topic']

    output = data['response']

    if output:
        for value in output:
            q = value['question']
            if value['AIML']:
                ret_text = generate_output(value['AIML'],q) + addTopic(topicText)
                split = False
            elif value['WEB']:
                ret_text = generate_output(value['WEB'].split(".")[0],q) + addTopic(topicText)

    response = data[u'ontologii']
    if response:
        ret_text = response

    q = topicText
    if ret_text is None and topicText:
        ret_text = generate_output(topicText,q)
    elif ret_text is None:
        q = random.choice(re.split('\n',listaMea))
        ret_text = generate_output(q,q)
    return ret_text


@route('/',method = 'POST')
def process():
    data = request.body.read()
    data = json.loads(data)

    raspuns = parseJson(data)
    return raspuns

run(host='localhost', port=7000, debug=True)
