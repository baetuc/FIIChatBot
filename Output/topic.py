"""
Modul creat de Andrei Iacob grupa 3A5

Modulul se ocupă cu generarea unui topic bazat pe hipernime.
"""
from nltk.corpus import wordnet as wn

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
