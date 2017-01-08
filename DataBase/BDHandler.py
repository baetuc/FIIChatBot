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
        topic = sentences["topic"]
        subtopic = sentences["subtopic"]
        
        Ontologii.jsonConverterAndInserter(data)
        print 'AIML'
        responseAIMLsentence = AIML.getResponse(sentence)

        print 'AIML topic'

        if responseAIMLsentence != 'I have no answer for that.':
            responseAIML = responseAIMLsentence
        else:
            responseAIML = None
        
        if responseAIML is None:  
            responseAIMLtopic = AIML.getResponseForTopic(topic)
            responseAIMLsubtopic = AIML.getResponseForTopic(subtopic)

            if responseAIMLtopic != 'I have no answer for that.':
                responsetopic = responseAIMLtopic
            else:
                if responseAIMLsubtopic != 'I have no answer for that.':
                    responsetopic = responseAIMLsubtopic
                else:
                    responsetopic = None 

        print 'web'
        if responsetopic is None:
            gooAnswer = searchWeb.get_google_answer(sentence)
            
            if gooAnswer is not None:
                responseWeb = gooAnswer
            else:
                gooAnswerSumm = searchWeb.get_google_summary(sentence)
                if gooAnswerSumm is not None:
                    responseWeb = gooAnswerSumm
                else:
                    try:
                        wikiAnswer = searchWeb.Wiki(sentence)
                    except:
                        wikiAnswer = None

                    if wikiAnswer:    
                        responseWeb = wikiAnswer
                    else:
                        responseWeb  = None
                        
            
        print 'ont'

        responseOntologii = None
        if responseWeb is None:

            responseOntologiiTopic = Ontologii.getWords(topic, subtopic)
            if responseOntologiiTopic is not None:
                responseOntologii = responseOntologiiTopic

        r = {"question":sentence, "AIML":responseAIML, "WEB":responseWeb}
        response.insert(index, r);


    dictionaryToJson = json.dumps({"response":response, "ontologii": responseOntologii, "topic": responsetopic})

    return dictionaryToJson
