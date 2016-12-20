"""
Modul creat de Moisii Cosmin grupa 3A5

Încarcă un xlsx cu întrebări și alege una random.

Pentru cazul în care răspuns-ul de pe internet nu este suficient se poate genera o întrebare.
"""


import pyexcel_xls
from random import randrange
data = pyexcel_xls.get_data("questions.xlsx")
#https://www.reddit.com/r/trivia/comments/3wzpvt/free_database_of_50000_trivia_questions/
number_of_sheets = len(data)
name_of_sheets = []
for i in data:
    name_of_sheets.append(i)
number_of_questions = list()
for i in range(number_of_sheets):
    number_of_questions.append(len(data[name_of_sheets[i]]))
#print data["3 Answers"][5][3]
def generate_question():
    sheet = randrange(0, number_of_sheets)
    question = randrange(1, number_of_questions[sheet])
    print(data[name_of_sheets[sheet]][question][0])
    return data[name_of_sheets[sheet]][question][0]