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

def showDatabase():
    global C
    openDatabase()
    for row in C.execute('SELECT * FROM words') :
        print row
    closeDatabase()

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
    openDatabase()
    C.execute("DROP TABLE words")
    closeDatabase()



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
    print '1'
    if openDatabase() == False :
        return
    for row in C.execute("SELECT word,synonym,type FROM words WHERE topic='{0}'".format(topic)):
        rows.append(row)
    print '2'
    if len(rows) is 0:
        for row in C.execute("SELECT word,synonym,type FROM words WHERE subtopic='{0}'".format(subtopic)):
            rows.append(row)
        if len(rows) is 0:
            print "not topic or subtopic"
            closeDatabase()
            return None
    print '3'
    closeDatabase()
    vb = []
    past_verb = []
    present_verb = []
    adjective = []
    custom_adjective = []
    noun = []
    custom_noun = []

    for row in rows:
        if row[2] == PARTS_OF_SPEECH['verb'] :
            vb.append(row[1])
        if row[2] == PARTS_OF_SPEECH['past_verb'] :
            past_verb.append(row[1])
        if row[2] == PARTS_OF_SPEECH['present_verb'] :
            present_verb.append(row[1])
        if row[2] == PARTS_OF_SPEECH['adjective'] :
            adjective.append(row[1])
        if row[2] == PARTS_OF_SPEECH['custom_adjective'] :
            custom_adjective.append(row[1])
        if row[2] == PARTS_OF_SPEECH['noun'] :
            noun.append(row[1])
        if row[2] == PARTS_OF_SPEECH['custom_noun'] :
            custom_noun.append(row[1])
    print '4'
    toReturn = {}
    
    if len(vb) :
        toReturn['verb'] = []
        toReturn['verb'].append(random.choice(vb))
    print '5'
    if len(past_verb) :
        toReturn['past_verb'] = []
        toReturn['past_verb'].append(random.choice(past_verb))
    print '6'
    if len(present_verb) :
        toReturn['present_verb'] = []
        toReturn['present_verb'].append(random.choice(present_verb))
    print '7'
    if len(noun) :
        toReturn['noun'] = []
        toReturn['noun'].append(random.choice(noun))
    print '8'
    if len(custom_noun) :
        toReturn['custom_noun'] = []
        toReturn['custom_noun'].append(random.choice(custom_noun))
    print '9'
    if len(adjective) :
        toReturn['adjective'] = []
        toReturn['adjective'].append(random.choice(adjective))
    print '10'
    if len(custom_adjective) :
        toReturn['custom_adjective'] = []
        toReturn['custom_adjective'].append(random.choice(custom_adjective))

    print "Found words"
    print toReturn
    return toReturn

getWords('danceaa', 'sport')
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
        

closeDatabase()


## how to execute it 
#jsonConverterAndInserter('input.json')


## only for testing functionality



