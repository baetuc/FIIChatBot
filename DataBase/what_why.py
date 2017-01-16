"""
Modul creat de Andrei Mazareanu, Dragos Lucaniuc grupa 3A5
Modulul se ocupa de doua feluri de intrebari:
1. What is your favorite X?
2. Why is X your favorite?
Singurul motiv pentru care sunt puse in acelasi fisier e ca sa nu ne complicam asa mult la integrare
"""

PORT = 8000
import re
import random
class FavoriteHandler:
    def __init__(self):
        """
        Clasa care se ocupa cu intrebari de tipul "What is your favorite X"
        """
        self._given_answers = {}
        self._given_reasons = {}
        self._domains = {
            "color" : ["blue", "red", "orange", "cyan", "black"],
            "food" : ["pizza", "hamburger", "salad", "sushi", "soup"],
            "car" : ["Ford", "Mercedes", "Ferrari", "Dacia", "BMW", "Honda"],
            "song" : ["You make me wanna", "We are Young", "Rainbow in the Dark", "Stayin Alive"],
            "band|artist" : ["Iron Maiden", "Eminem", "The Beatles", "ABBA"],
            "drink" : ["Water", "Beer", "Wine", "Vodka!"],
            "book" : ["The Lord of The Rings", "The Da Vinci Code", "Harry Potter", "50 Shades of Grey"],
            "movie" : ["Inception", "Django Unchained", "Seven Samurai", "Argo"],
            "TV show" : ["Breaking Bad", "Game of Thrones", "Doctor Who", "South Park"],
            "actor" : ["Tom Hanks", "Danny de Vito", "Robert de Niro", "Keanu Reeves"],
            "actress" : ["Scarlett Johansson", "Cate Blanchett", "Jennifer Lawrence", "Natalie Portman"],
            "site" : ["Google", "Youtube", "Facebook", "Reddit"],
            "activity|leisure" : ["Hiking", "Surfing the web", "Playing video games"],
            "animal|pet" : ["Cat", "Dog", "Turtle", "Bird"],
            "brand|company" : ["Coca Cola", "Apple", "Microsoft", "Nestle"],
            "country" : ["Romania", "Germany", "United States of America", "Japan"],
            "school subject" : ["Artificial Intelligence", "Mathematics", "English"],
            "language" : ["English", "Romanian", "German", "Japaneese"],
            "sport" : ["Football", "Baseball", "Running", "Boxing"],
            "team" : ["Manchester United", "Real Madrid", "NY Yankers"],
            "holiday" : ["Christmas", "New Year", "Easter"],
            "number" : ["1","3","7","9","13"],
            "soda" : ["Cocal Cola", "7Up", "Mountain Dew"],
            "video game|computer game" : ["Counter Strike", "Overwatch", "Half Life"],
            "author|writer|poet" : ["Edgar Allan Poe", "J.R.R. Tolkien","J.K. Rowling"]
        }
        self._reasons = {
            "color" : {
                "blue" : ["It reminds me of the sky", "I think it's a calming color. I even painted my room that color!", "It reminds me of a little baby boy"],
                "red" : ["I think it's a really powerful color", "It reminds me of the sunset", "I think it gives me energy!"],
                "orange" : ["It reminds me of a summer sunset", "I really like the fruit with the same name I guess", "I think i look well in orange."],
                "cyan" : ["It's a special color", "Not too many people think of cyan as their favorite color!", "It looks brilliant"],
                "black" : ["I find it oddly soothing", "It makes me sleepy", "I think it's an elegant color"]
            },
            "food" : {
                "pizza" : ["It's yummy!", "It's nice to eat at parties", "You can order it and eat without needing to leave home or cook"],
                "hamburger" : ["I really like beef", "It's preety quick to cook", "I know a really nice burger joint"],
                "salad" : ["I doesn't make you fat", "I think it's very fresh", "It doesn't need any meat to be good"],
                "sushi" : ["It's a lean food", "I really like fish", "I think it's exotic"],
                "soup" : ["It also hydrate you", "I really like vegetabl soup", "You can just throw anything into boiling water and you're done"]
            },
            "car" : {
                "Ford" : ["They are really cheap and good", "They have both average-Joe cars, and things like the Mustang", "I really like how the gears change"],
                "Mercedes" : ["I think they are really luxurious", "I think they are really well build", "I think the rear-wheel drive it's a big plus"],
                "Ferrari" : ["I like fast cars","Why wouldn't I? ","I allways wanted a Ferrari"],
                "Dacia" : ["I like romanian cars","I think it is affordable and suited for our roads"],
                "BMW" : ["I like fast and good looking cars","It represents the perfect harmony between elegance, comfort and dynamism"],
                "Honda" : ["They have a low fuel consumption and a lot a systems","I like Asian cars"],
            },
            "song" : {
                "You make me wanna" : ["I got married to this song", "It gives me energy"],
                "We are young" : ["I have a young spirit and this song describes me (wink)", "It is a song full of energy"],
                "Rainbow in the Dark" : ["This is my rock side", "I think it is the best rock/heavy metal voice ever"],
                "Stayin alive" :["This would be the first song on my mixtape for a zombie apocalypse", "I think it is a great funeral song (joke)"],
            },
            "band|artist" : {
                "Iron Maiden" : ["Who doesn't like them?!", "I really like heavy metal"],
                "Eminem" : ["I like his style", "I like the lyrics"],
                "The Beatles" : ["I like good music", "Probably the best band of all time"],
                "ABBA" : ["The best music was from the good old days","I sing their songs in the shower, every word"],
            },
            "drink" : {
                "Water" :["It keeps me alive!", "I can'y live without it"],
                "Beer" :["Beer it's just Beer, what is not to love about it?", "I like the taste"],
                "Wine" :["I like the taste", "It helps you travel the World in a bottle"],
                "Vodka" :["Nothing like a good old bottle of Rubinoff or Zelcos.", "It helps me reset my memory"],
            },
            "book" : {
                "The Lord of The Rings" : ["I like the story", "I like the characters", "I really like how the places are described"],
                "The Da Vinci Code" : ["I like how it chalanges religion", "I really like the main character", "I like how Dan Brown writes"], 
                "Harry Potter": ["I loved the book when I was a kid", "I like both the book and the movie", "I love the author"], 
                "50 Shades of Grey" : ["You don't want to know", "I hope I'll find a Mr. Grey some day", "It's a spicy book"],
            "soda" : {
            	"Coca Cola" : ["I prefer to drink it instead of coffee", "I like the pretty bottle", "It's nice to cool off in the summer"],
            	"7Up" : ["It's better than Sprite", "I like that it's not that sweet", "It's really bubbly"],
            	"Mountain Dew" : ["It's yellow", "It's better than Coke", "It has a really nice taste"]
            },
            "video game|computer game" : {
            	"Counter Strike" : ["It's a game that is still good after all these years", "Everyone who likes games has played CS at least once", "I love how a mod came so far"],
            	"Overwatch" : ["It combines the MOBA and FPS genres", "The characters are really balanced", "I like to play with my team"],
            	"Half Life" : ["I think it revolutionized the genre", "It had really good graphics for it's age", "I like the story"]
            },
            "author|writer|poet" : {
            	"Edgar Allan Poe" : ["I like poetry", "I really like 'The Raven'", "I really like his symbolism"],
            	"J.R.R. Tolkien" : ["I really like The Hobbit!", "I love The Lord of the Rings", "I like how he created a huge world by writing"],
            	"J.K. Rowling" : ["I grew up with Harry Potter", "I really like her style of writing", "Everyone loves Harry Potter!"]
            }
        }
    }
    
    def _get_known_domain(self, question):
        for domain in self._domains:
            r = ".*(" + domain + ").*"
            if re.match(r, question, re.IGNORECASE):
                return domain
        return None
    
    def _get_unknown_domain(self, question):
        r = ".*what.*(favorite|favourite) ([a-zA-Z]+).*"
        m = re.match(r,question,re.IGNORECASE)
        if m and m.group(1):
            return m.group(1)
        return None

    def is_favorite_question(self, question):
        if "what" in question.lower() and ("favorite" in question.lower() or "favourite" in question.lower()):
            return True
        return False

    def _get_answer_from_domain(self, domain):
        if self._given_answers.get(domain):
            return "I already told you my favorite is %s"%(self._given_answers.get(domain))
        else:
            response = random.choice(self._domains.get(domain))
            self._given_answers[domain] = response
            real_domain = domain
            if "|" in domain:
                real_domain = domain.split("|")[0]
            return "My favorite %s is %s"%(real_domain, response)

    def answer_what(self, question):
        if not self.is_favorite_question(question):
            return "Honestly, I don't know what to say"
        domain = self._get_known_domain(question)
        if domain:
            answer = self._get_answer_from_domain(domain)
            return answer
        else:
            domain = self._get_unknown_domain(question)
            if domain:
                return "I don't think I have a favorite %s"%(domain)
            else:
                return "Honestly, I don't know what to say"

    def is_why_question(self, question):
        if "why" in question.lower() and ("favorite" in question.lower() or "favourite" in question.lower()):
            return True
        return False

    def _get_query_from_what_question(self, question):
        r = ".*why.*is ([a-zA-Z]+).* your (favorite|favourite).*"
        m = re.match(r, question, re.IGNORECASE)
        if m and m.group(1):
            return m.group(1)
        return None

    def answer_why(self, question):
        if not self.is_why_question(question):
            return "Honestly, I don't know what to say"
        query = self._get_query_from_what_question(question)
        if query:
            answer_given = False
            for domain in self._domains:
                if self._given_answers.get(domain) == query:
                    answer_given = True
                    break

            if not answer_given:
                return "I didn't say that was my favorite!"

            given_reason = self._given_reasons.get(query)
            if given_reason:
                return "I already told you that!"
            given_reason = random.choice(self._reasons.get(domain).get(query))
            self._given_reasons[query] = given_reason
            return given_reason
        return "I don't really have a favorite"

if __name__ == "__main__":
    import subprocess
    from bottle import run, post, request, response, get, route, Bottle
    fh = FavoriteHandler()

    @route('/', method='POST')
    def process():
        x = request.body.read().decode("utf-8") 
        import json
        x = json.loads(x)
        if x.get("action") == "answer_why":
            r = fh.answer_why(x.get("question"))
            print(r)
            return {"ans" : r}
        elif x.get("action") == "is_why_question":
            r = fh.is_why_question(x.get("question"))
            print(r)
            return {"ans" : r}

        elif x.get("action") == "answer_what":
            r = fh.answer_what(x.get("question"))
            print(r)
            return {"ans" : r}
        elif x.get("action") == "is_favorite_question":
            r = fh.is_favorite_question(x.get("question"))
            print(r)
            return {"ans" : r}
        else:
            return {"ans" : "Unknown action"}
    run(host='localhost', port=PORT, debug=True)

