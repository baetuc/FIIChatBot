j = '{"is_negation": "false", "words": [["you", "PRP", []], ["think", "VB", ["believe", "consider", "conceive"]], ["i", "JJ", ["iodine", "iodin", "atomic_number_53"]], ["get", "VBP", ["acquire", "become", "go"]], ["out of the blue", "J", []]], "type": "question", "sentence": "do you think i got here out of the blue?"}'

mineWords = ["mine","i","myself","my"]
conn = sqlite3.connect('ontology.db')

c = conn.cursor()
try:
    c.execute("DROP TABLE words")
except :
    print()
c.execute('''CREATE TABLE words(id INTEGER PRIMARY KEY AUTOINCREMENT, word text, type text)''')

def insertWord(word,type) :
    c.execute("INSERT INTO words (word,type) VALUES ('{0}','{1}')".format(word,type))
    conn.commit()

def jsonConverterAndInserter(JSON, function) :
    global mineWords
    data = json.loads(JSON)
    flag = 0
    sentence = data["sentence"].split(" ")
    for my in mineWords:
        if my in sentence:
            flag = 1
    if flag != 0:
        for x in data["words"]:
            function(x[0],x[1])

jsonConverterAndInserter(j, insertWord)

for row in c.execute('SELECT * FROM words'):
    print(row)

conn.close()
