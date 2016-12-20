import simplejson

import searchWeb
import AIML
#import Ontologii

def init(data):
    
    numberS = int(data["numberSentences"])
    responsServ = " "
    for index in range(numberS):
        sentences = data["sentences"][index]
        sentence = sentences["sentence"]
        type = sentences["type"]
        is_negation = sentences["is_negation"]
        words = sentences["words"]
        
        responseAIML = AIML.getResponse(sentence)

        if responseAIML != "I have no answer for that.":
            data["response_AIML"] = responseAIML     
        else:
            gooAnswer = searchWeb.get_google_answer(sentence)
            if gooAnswer is not None:
                data["response_Goo"] = gooAnswer 
            else:
                wikiAnswer = searchWeb.Wiki(sentence)
                gooAnswerSumm = searchWeb.get_google_summary(sentence)
                data["response_GooSum"] = gooAnswerSumm
                data["response_Wiki"] = wikiAnswer 


                
            #links -n
            #print searchWeb.get_google_links(sentence)
            #response -n
            #print searchWeb.get_google_response(sentence)
            #responce from summary - k
            #print searchWeb.get_google_summary(sentence)
            #specific answers - k - "None"
            #print searchWeb.get_google_answer(sentence)
            #google references
            #print searchWeb.get_google_citeations(sentence)
            #wiki answer - porsonality - k
            #print searchWeb.Wiki(sentence)
    simplejson.dumps(data)
    return data
