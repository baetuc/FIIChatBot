"""
Modul creat de Moisii Cosmin grupa 3A5

Modulul transformă o întrebare enunțiativă în una interogativă/
"""

def declarative_to_interrogative (inputStr):

    tokens = nltk.PunktWordTokenizer().tokenize(inputStr)
    tagged = nltk.pos_tag(tokens)
    auxiliary_verbs = [i for i, w in enumerate(tagged) if w[1] == 'VBP']
    if auxiliary_verbs:
        tagged.insert(0, tagged.pop(auxiliary_verbs[0]))
    else:
        tagged.insert(0, ('did', 'VBD'))
    tagged.insert(0, ('When', 'WRB'))

    return ' '.join([t[0] for t in tagged])