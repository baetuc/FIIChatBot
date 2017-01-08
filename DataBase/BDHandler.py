import simplejson
import json
import searchWeb
import AIML
import Ontologii
response= []
def init(data):
    
    numberS = int(data["number_of_sentences"])
    responsServ = " "
    for index in range(numberS):
        sentences = data["sentences"][index]
        sentence = sentences["sentence"]
        type = sentences["type"]
        is_negation = sentences["is_negation"]
        words = sentences["words"]
        #topic = sentences["topic"]

        #Ontologii.jsonConverterAndInserter(data)
        responseAIML = AIML.getResponse(sentence)
        #responseAIMLtopic = AIML.getResponseForTopic(topic)

        data["response_AIML"] = responseAIML
        #data["response_AIMLtopic"] = responseAIMLtopic  

        gooAnswer = searchWeb.get_google_answer(sentence)
        
        if gooAnswer is not None:
            data["response_Goo"] = gooAnswer
            responseAI = gooAnswer
        else:
            gooAnswerSumm = searchWeb.get_google_summary(sentence)
            if gooAnswerSumm is not None:
                responseAI = gooAnswerSumm
            else:
                try:
                    wikiAnswer = searchWeb.Wiki(sentence)
                except:
                    wikiAnswer = None

                if wikiAnswer:    
                    responseAI = wikiAnswer
                else:
                    responseAI  = None


        r = {"question":sentence, "AIML":responseAIML, "AI":responseAI, "index":index}
        response.insert(index, r);


    dictionaryToJson = json.dumps({"response":response})

    return dictionaryToJson
