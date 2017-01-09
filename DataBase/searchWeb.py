from bs4 import BeautifulSoup
import  requests, re
import wikipedia
import google


def html_to_text(html):
    soup = BeautifulSoup(html, "html.parser")
    for script in soup(["script", "style"]):
        script.extract()
    return(soup.get_text())
                
def get_google_links(question,num=1):
    urls=google.search("question")
    i = 0
    text=""
    for url in urls:
        if i < num:
            text=text+google.get_page(url)
            i+=1
        else:
            break
    return (text)
       
def get_google_response(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text.encode('UTF-8')
    return (html_to_text(content))

def get_google_summary(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text.encode('UTF-8')
    summary=re.findall('<div class="_tXc">.*<[/]div>',content)
    if len(summary) is not 0:
        return (html_to_text(summary[0]))
    else:
        return(None)
        
def get_google_answer(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text.encode('UTF-8')
        
    answer=re.findall('<div class="_XWk">.*?<[/]div>',content)       #E.g. What is the president of India
    answer2=re.findall('<div class="_Tfc _j0k">.*?<[/]div>',content) #How fast is a cheetah?

    if len(answer) > 0:
        if len(answer2) > 0:
            return (html_to_text(answer[0])+' '+html_to_text(answer2[0]))
        return (html_to_text(answer[0]))
    
    answer=re.findall('<span class="_m3b".*?<[/]span>',content)  #calculator
    if len(answer) > 0:
        return (html_to_text(answer[0]))    
        
    answer=re.findall('<div class="kltat">.*?<[/]div>',content)       #what is the longest river in the world
    answer2=re.findall('<div class="ellip klmeta">.*?<[/]div>',content)

    if len(answer) > 0:
        if len(answer2) > 0:
            return (html_to_text(answer[0])+' '+html_to_text(answer2[0]))
        return (html_to_text(answer[0]))
        
    answer=re.findall('<span class="cwcot".*?<[/]span>',content)  #calculator
    if len(answer) > 0:
        return (html_to_text(answer[0]))
        
    answer=re.findall('<span class="nobr"><h2 class="r".*?<[/]span>',content)  #calculator
    if len(answer) > 0:
        return (html_to_text(answer[0]))
    return None

def Wiki(text):
    try:
        response = wikipedia.summary(text, sentences=2)
    except:
        response = None
    return response