import random

class Ontologie():

    def __init__(self):
        self.MINE_WORDS = ["mine","i","myself","my","me"]
        self.data = dict()
        self.dataCount = 0
        self.synonyms = dict()
        self.tempData = None

    def _new_word(self,word,synonyms,pos):
        if not self.tempData:
            self.tempData = []
        if word not in self.synonyms.keys():
            self.synonyms[word] = []

        self.tempData.append((word,pos))
        self.synonyms[word] = synonyms

    def _insert_sentence(self):
        self.dataCount += 1
        self.data[self.dataCount] = self.tempData
        self.tempData = None

    def _print_structure(self): #debug
        print(self.data)
        print(self.dataCount)
        print(self.synonyms)

    def _answer_question(self,sentence):
        ret = ""
        words = sentence['words']
        maxScore = 0
        max_match = None
        for match in self.data:
            score = 0
            for word in self.data[match]:
                for word2 in words:
                    if word2['word'] == word[0]:
                        score+=2
                        if word[0] in self.synonyms[word2['word']]:
                            score+=1
            if score > maxScore:
                maxScore = score
                max_match = match
            if score == maxScore and random.random()<0.5:
                maxScore = score
                max_match = match
        if max_match:
            ret = "You "
            setA = set([x[0] for x in self.data[max_match]])
            setB = set(sentence['sentence'].replace("?","").replace(".","").split(' '))
            print(setA)
            print(setB)
            diff = setA.symmetric_difference(setB)

            for X in self.data[max_match]:
                if X[0] not in self.MINE_WORDS:
                    ret += (X[0]+' ')
                if X[0] == "my":
                    ret += "your "
                if X[0] == "go":
                    ret += "are going"
        return ret

    def new_data(self,data):
        return_data = ""
        for sentence in data['sentences']:
            flag = 0
            for mw in self.MINE_WORDS:
                if mw in sentence['sentence']:
                    flag = 1
            if flag == 0:
                continue
            if sentence['type'] == 'question':
                return_data += self._answer_question(sentence)
                continue
            words = sentence['words']
            for word in words:
                self._new_word(word['word'],word['synonyms'],word['part_of_speech'])
            self._insert_sentence()
        if return_data == "":
            return_data = None
        return return_data
