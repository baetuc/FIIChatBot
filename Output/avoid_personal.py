"""
		Modul creat de Paius Paraschiv-Catalin

		Avoid personal answers (Question contains "you") considering a low probability for this action

		In cazul in care intrebarea contine pronumele "you" si avand la dispozitie o probabilitate constanta,
	stabilim daca dorim sa raspundem la intrebare sau daca evitam raspunsul (e.g. o glumita, o intrebare catre user)
"""
import json, random

youData = ["you", "your", "yours", "yourself"]

global_answers = ["Sorry dude, I have just met you. You will find out more things about me in time.",
	"Hehe, you are smart. But I will not answer this time, sorry.",
	"Maybe if you bring me some beer, I will answer this as well.",
	"Questions, question and more questions. Tell me a good joke.",
	"Try again with more confidence, maybe I will answer you next time.",
	"Let me tell you something hilarious about me. I still believe in Santa. I saw him this Christmas."]

#@Param data - JSON content
#@Return - JSON data
def avoid_personal(data):
	data = json.loads(data)
	if random.random() > 0.1:
		return None
	sentences = data["text_processing"]["sentences"]
	for sentence in sentences:
		if sentence["type"] == "question":
			for word in sentence["words"]:
				if word["word"] in youData:
					return random.choice(global_answers)
	return None
