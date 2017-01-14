"""
		Modul creat de Paius Paraschiv-Catalin

		Avoid personal answers (Question contains "you") considering a low probability for this action

		In cazul in care intrebarea contine pronumele "you" si avand la dispozitie o probabilitate constanta,
	stabilim daca dorim sa raspundem la intrebare sau daca evitam raspunsul (e.g. o glumita, o intrebare catre user)
"""
import json, random

global_answers = ["Sorry dude, I have just met you. You will find out more things about me in time.",
	"Hehe, you are smart. But I will not answer this time, sorry.",
	"Maybe if you bring me some beer, I will answer this as well.",
	"Questions, question and more questions. Tell me a good joke.",
	"Try again with more confidence, maybe I will answer you next time.",
	"Let me tell you something hilarious about me. I still believe in Santa. I saw him this Christmas."]

"""
global_questions = ["",
	"",
	""]
"""

#@Param data - JSON content
#@Return - JSON data
def avoid_personal(data):
	data = json.loads(data)
	data["avoid_personal"] = None
	if random.random() > 0.1:
		return json.dumps(data)
	sentences = data["text_processing"]["sentences"]
	for sentence in sentences:
		if sentence["type"] == "question":
			for word in sentence["words"]:
				if word["word"] == "you":
					data["avoid_personal"] = random.sample(global_answers, 1)[0]
		"""
		else:
			for word in sentence["words"]:
				if word["word"] == "you":
					data["avoid_personal"] = random.sample(global_questions, 1)[0]
		"""
	return json.dumps(data)