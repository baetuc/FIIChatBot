import json
import aiml
data = open("test.json","r").read()
d = json.loads(data)
#print (d.get("sentence"))
sentence=d.get("sentence")
topic=d.get("topic")

def eliminaSemne(sentence):
    semne = ";:,."
    for i in semne:
        if i in sentence:
            sentence = sentence.replace(i,"")
    return sentence
#print(eliminaSemne("Mmmm, ce frumos ninge!"))
#print(eliminaSemne(sentence))


# Create the kernel and learn AIML files
kernel = aiml.Kernel()
kernel.learn("std-startup.xml")
kernel.respond("load aiml b")


def getResponse(question):
    response = kernel.respond(eliminaSemne(question))
    return response

def getResponseForTopic(topic):
    if topic is not None:
        response = kernel.respond(eliminaSemne(topic))
    else:
        response = kernel.respond("random")


    if "I have no answer for that" in response:
        response = kernel.respond("random")
    return response


#print(getResponse(eliminaSemne("Happy ,birthday")));
#print(getResponse(topic));
print(getResponseForTopic('sport'));


