"""
		Modul creat de Paius Paraschiv-Catalin

		Cheer UP for negative sentiments

		In cazul depistarii unui sentiment negativ, functia returneaza un raspuns / o intrebare 
	ce ar putea inveseli utilizatorul (e.g. o incurajare, o mica glumita, o invitatie la bere etc)
"""
import httplib, urllib
import json, random

global_answers = ["Why aren't you more optimistic? Life is wonderfull.",
	"It will be just fine. Just believe in your own strength.",
	"Here's a joke. My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away.",
	"Here's a funny story about my brother. He dreamt he was forced to eat a giant marshmallow. When he woke up, his pillow was gone.",
	"I know what can cheer you up. Two Elephants meet a totally naked guy. After a while one elephant says to the other: \"I really don't get how he can feed himself with that thing!\"",
	"Don't worry, be happy!",
	"I'd like to buy a new boomerang please. Also, can you tell me how to throw the old one away?",
	"Life is better when you smile.",
	"Never give up! You can be a hero.",
	"Even in this situation you should smile, bacause good things happen when you do it.",
	"Grab a beer and cheer up!",
	"You can get over this. Bad feeling are like rocks, you can throw them away.",
	"Aww, c'mon. You will talk to my hand if continue this way.",
	"If you think you are the only one with problems, think about mexicans when they heard about the new President of America.",
	"Let's take a break. Do you want to watch American Pie? It's about a smiling pie made in America."]

### Functie Creata de Moisii Cosmin
def get_sentiment(text):
    params = urllib.urlencode({'text': text})
    f = urllib.urlopen("http://text-processing.com/api/sentiment/", params)
    data = f.read()
    return data

#@Param data - JSON content
#@Return - JSON data
def cheer_up(data):
	data = json.loads(data)
	data["cheer_up"] = None
	if random.random() > 0.7:
		return json.dumps(data)
	inputData = data["ai1"]
	sentiment = get_sentiment(inputData)
	sentiment = json.loads(sentiment)
	if sentiment["label"] == "neg":
		if float(sentiment["probability"]["neg"]) >= 0.60:
			data['cheer_up'] = random.sample(global_answers, 1)[0]
	return json.dumps(data)
