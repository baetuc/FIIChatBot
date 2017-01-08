import sqlite3
import json

# j = '{"is_negation": "false", "words": [["you", "PRP", []], ["think", "VB", ["believe", "consider", "conceive"]], ["i", "JJ", ["iodine", "iodin", "atomic_number_53"]], ["get", "VBP", ["acquire", "become", "go"]], ["out of the blue", "J", []]], "type": "question", "sentence": "do you think i got here out of the blue?"}'
DATABASE = 'ontoloigii.db'
MINE_WORDS = ["mine","i","myself","my","i've","i'm"]
TABLES_CREATED = 0
CONN = 0
C = 0

    # c.execute("DROP TABLE words")

## open database connection
def openDatabase():
    global CONN,DATABASE
    try:
        CONN = sqlite3.connect(DATABASE)
        return True
    except:
        CONN = 0
        print "error connecting to the database !"
        return False

## initialize database
def createDatabaseTables():
    global C,CONN,TABLES_CREATED
    C = CONN.cursor()
    if TABLES_CREATED == 0:
        try:
            C.execute('''CREATE TABLE words(id INTEGER PRIMARY KEY AUTOINCREMENT, word text, synonym text ,type text)''')
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
def insertWord(word,synonym,type) :
    global CONN,C
    C.execute("INSERT INTO words (word,synonym,type) VALUES ('{0}','{1}','{2}')".format(word,synonym,type))
    CONN.commit()




## converts JSON file or string to array
def convert(JSON):
    try:
        with open(JSON) as json_data:
            return json.load(json_data)        
    except:
        try:
            return json.loads(JSON)
        except:
            return False



## can get as input a string json or a file json
## should be executed with default insertWord function 
def jsonConverterAndInserter(JSON, function = insertWord ) :
    global MINE_WORDS,C
    if openDatabase() == False :
        return
    if createDatabaseTables() == False :
        return

    data = convert(JSON)
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
                            function(word['word'],synonym,word['part_of_speech'])
        except :
            print "json doesn't have the corret format !"
    else :
        print 'error loading the json !'

    # for row in C.execute('SELECT * FROM words'):
    #     print(row)
    
    closeDatabase()



## how to execute it 
# jsonConverterAndInserter('bd_input.json')


## only for testing functionality



