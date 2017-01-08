import sqlite3
import json
import random

# j = '{"is_negation": "false", "words": [["you", "PRP", []], ["think", "VB", ["believe", "consider", "conceive"]], ["i", "JJ", ["iodine", "iodin", "atomic_number_53"]], ["get", "VBP", ["acquire", "become", "go"]], ["out of the blue", "J", []]], "type": "question", "sentence": "do you think i got here out of the blue?"}'
DATABASE = 'ontoloigii.db'
PARTS_OF_SPEECH={"verb":"VB","past_verb":"VBD","present_verb":"VBP","noun":"NN","custom_adjective":"J","adjective":"JJ","custom_noun":"N"}
MINE_WORDS = ["mine","i","myself","my","i've","i'm"]
TABLES_CREATED = 0
CONN = 0
C = 0

    

## open database connection
def openDatabase():
    global CONN,DATABASE,C
    try:
        CONN = sqlite3.connect(DATABASE)
        C = CONN.cursor()
        return True
    except:
        CONN = 0
        print "error connecting to the database !"
        return False

## initialize database
def createDatabaseTables():
    global C,CONN,TABLES_CREATED
    if TABLES_CREATED == 0:
        try:
            C.execute('''CREATE TABLE words(id INTEGER PRIMARY KEY AUTOINCREMENT, word text, synonym text ,type text ,topic text , subtopic text )''')
            TABLES_CREATED = 1
            return True
        except:
            TABLES_CREATED = 1
            return True

## close database connection
def closeDatabase():
    global CONN
    CONN.close()


## delete table words
def deleteTableWords():
    global C
    C.execute("DROP TABLE words")    



## insets data in database 
## you should modify it and the way is used to get different entries in the database
def insertWord(word,synonym,type,category,subcategory) :
    global CONN,C
    C.execute("INSERT INTO words (word,synonym,type,topic,subtopic) VALUES ('{0}','{1}','{2}','{3}','{4}')".format(word,synonym,type,category,subcategory))
    CONN.commit()




## converts JSON file or string to array
def convert(JSON):
    with open(JSON) as json_data:
            print json_data
    try:
        with open(JSON) as json_data:
            print json_data
            return json.load(json_data)        
    except:
        try:
            return json.loads(JSON)
        except Exception as e:
            print e
            return False

## get info from database
def getWords(topic, subtopic = None):
    global PARTS_OF_SPEECH,C
    rows = []
    if openDatabase() == False :
        return
    for row in C.execute("SELECT word,synonym,type FROM words WHERE topic='{0}'".format(topic)):
        rows.append(row)
    if len(rows) is 0:
        for row in C.execute("SELECT word,synonym,type FROM words WHERE subtopic='{0}'".format(subtopic)):
            rows.append(row)
        if len(rows) is 0:
            print "not topic or subtopic"
            closeDatabase()
            return None
    closeDatabase()
    vb = []
    past_verb = []
    present_verb = []
    adjective = []
    custom_adjective = []
    noun = []
    custom_noun = []
    for row in rows:
        if row[2] == PARTS_OF_SPEECH["verb"]:
            vb.append(row[1])
        if row[2] == PARTS_OF_SPEECH["past_verb"]:
            past_verb.append(row[1])
        if row[2] == PARTS_OF_SPEECH["present_verb"]:
            present_verb.append(row[1]) 
        if row[2] == PARTS_OF_SPEECH["adjective"]:
            adjective.append(row[1])
        if row[2] == PARTS_OF_SPEECH["custom_adjective"]:
            custom_adjective.append(row[1])
        if row[2] == PARTS_OF_SPEECH["noun"]:
            noun.append(row[1])
        if row[2] == PARTS_OF_SPEECH["custom_noun"]:
            custom_noun.append(row[1])
    toReturn = {}
    if len(vb) :
        toReturn['verb'] = []
        toReturn['verb'].append(random.choice(vb))
        aux = random.choice(vb)
        while aux in toReturn['verb']:
            aux = random.choice(vb)
        toReturn['verb'].append(aux)

    if len(past_verb) :
        toReturn['past_verb'] = []
        toReturn['past_verb'].append(random.choice(past_verb))
        aux = random.choice(past_verb)
        while aux in toReturn['past_verb']:
            aux = random.choice(past_verb)
        toReturn['past_verb'].append(aux)                          

    if len(present_verb) :
        toReturn['present_verb'] = []
        toReturn['present_verb'].append(random.choice(present_verb))
        aux = random.choice(present_verb)
        while aux in toReturn['present_verb']:
            aux = random.choice(present_verb)
        toReturn['present_verb'].append(aux)

    if len(noun) :
        toReturn['noun'] = []
        toReturn['noun'].append(random.choice(noun))
        aux = random.choice(noun)
        while aux in toReturn['noun']:
            aux = random.choice(noun)
        toReturn['noun'].append(aux)

    if len(custom_noun) :
        toReturn['custom_noun'] = []
        toReturn['custom_noun'].append(random.choice(custom_noun))
        aux = random.choice(custom_noun)
        while aux in toReturn['custom_noun']:
            aux = random.choice(custom_noun)
        toReturn['custom_noun'].append(aux)

    if len(adjective) :
        toReturn['adjective'] = []
        toReturn['adjective'].append(random.choice(adjective))
        aux = random.choice(adjective)
        while aux in toReturn['adjective']:
            aux = random.choice(adjective)
        toReturn['adjective'].append(aux)   

    if len(custom_adjective) :
        toReturn['custom_adjective'] = []
        toReturn['custom_adjective'].append(random.choice(custom_adjective))
        aux = random.choice(custom_adjective)
        while aux in toReturn['custom_adjective']:
            aux = random.choice(custom_adjective)
        toReturn['custom_adjective'].append(aux)

    print toReturn
    return toReturn

getWords('aas')
## can get as input a string json or a file json
## should be executed with default insertWord function 
def jsonConverterAndInserter(JSON, function = insertWord ) :
    global MINE_WORDS,C
    if openDatabase() == False :
        return

    if createDatabaseTables() == False :
        return
    data = JSON
    if data != False:
        try:
            for sentence in data['sentences']:
                words = sentence['sentence'].split(' ')
                flag = 0
                for mw in MINE_WORDS:
                    if mw in words:
                        flag = 1
                if flag != 0 :
                    for word in sentence['words']:
                        for synonym in word['synonyms']:
                            function(word['word'],synonym,word['part_of_speech'],sentence['topic'],sentence['subtopic'])
        except :
            print "json doesn't have the corret format !"
    else :
        print 'error loading the json !'
        
#    for row in C.execute('SELECT * FROM words'):
#        print(row)    
    closeDatabase()
    return True

    


## how to execute it 
#jsonConverterAndInserter('input.json')


## only for testing functionality



