import aiml
import os
import json


class BD_AIML:
    def __init__(self):
        self.bot_kernel = aiml.Kernel()
        module_file_name = "."
        brain_file_name = "bot_Brain.brn"
        aimls_folder_name = "aiml"
        bot_properties_file_name = "bot.properties"

        brain_file_path = os.path.join(module_file_name, brain_file_name)
        aimls_folder_path = os.path.join(module_file_name, aimls_folder_name)
        bot_properties_file_path = os.path.join(module_file_name,
                                                bot_properties_file_name)

        if os.path.isfile(brain_file_path):
            self.bot_kernel.loadBrain(brain_file_path)
        else:
            for subdir, dirs, files in os.walk(aimls_folder_path):
                for aiml_file in files:
                    self.bot_kernel.learn(os.path.join(subdir, aiml_file))
            self.bot_kernel.saveBrain(brain_file_path)

        properties_file = open(os.path.join(os.getcwd(),
                                            bot_properties_file_path))
        for line in properties_file:
            parts = line.split('=')
            key = parts[0]
            value = parts[1][:-1] #to remove \n from string final
            self.bot_kernel.setBotPredicate(key, value)

    def respond(self, input_statement, session_id=1):
        return self.bot_kernel.respond(input_statement, session_id)


bd= BD_AIML()
data = open("test.json","r").read()
d = json.loads(data)
sentence=d.get("sentence")
topic=d.get("aatopic")


def eliminaSemne(sentence):
    semne = ";:,."
    for i in semne:
        if i in sentence:
            sentence = sentence.replace(i,"")
    return sentence

def getResponse(question):
    response = bd.respond(eliminaSemne(question))
    return response

def getResponseForTopic(topic):
    if topic is not None:
        response = bd.respond(eliminaSemne(topic))
    else:
        response = bd.respond("random")

    if "I have no answer for that" in response:
        response = bd.respond("random")
    return response

# print(getResponse(eliminaSemne("Happy ,birthday")));
# print(getResponseForTopic(topic));
# print(getResponse("Hello"));
# print(getResponse("My name is Mirela"));
# print(getResponse("What is my name?"));
# print(getResponse("Hi"));
# print(getResponse("Who are you?"));
#
# print(getResponse("When is your birthday?"))



