import json
import aiml
data = open("test.json","r").read()
d = json.loads(data)
#print (d.get("sentence"))


sentence=d.get("sentence")

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
    response = kernel.respond(question)
    return response

print(getResponse(eliminaSemne("Happy ,birthday")));


