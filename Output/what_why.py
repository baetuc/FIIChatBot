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
            "soda" : ["Cocal Cola", "7Up", "Mountan Dew"],
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
                "Mercedes" : ["I think they are really luxurious", "I think they are really well build", "I think the rear-wheel drive it's a big plus"]
                #to be continued
            }
        }
    
    def _get_known_domain(self, question):
        for domain in self._domains:
            r = ".*(" + domain + ").*"
            if re.match(r, question, re.IGNORECASE):
                return domain
        return None
    
    def _get_unknown_domain(self, question):
        r = ".*what.*favorite ([a-zA-Z]+).*"
        m = re.match(r,question,re.IGNORECASE)
        if m and m.group(1):
            return m.group(1)
        return None

    def is_favorite_question(self, question):
        if "what" in question.lower() and "favorite" in question.lower():
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
        if "why" in question.lower() and "favorite" in question.lower():
            return True
        return False
    
    def _get_query_from_what_question(self, question):
        r = ".*why.*is ([a-zA-Z]+).* your favorite.*"
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
