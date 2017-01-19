"""
Modul creat de Andrei Iacob grupa 3A5

Modulul se ocupă cu căutare pe Google
"""

from bs4 import BeautifulSoup
import  requests, re

def html_to_text(html):
    soup = BeautifulSoup(html)
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out
    return(soup.get_text())
                

import google
  
def get_google_links(question,num=2):
    urls=google.search("what is the capital of Germany?")
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
    content = r.text
    print(content)
    return (html_to_text(content))

def get_google_summary(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text
    summary=re.findall('<div class="_tXc">.*<[/]div>',content)
    if len(summary) is not 0:
        return (html_to_text(summary[0]))
    summary=re.findall('<ol class="_l0g">.*?<[/]ol>',content)
    if len(summary) is not 0:
        return (html_to_text(summary[0]))
    summary=re.findall('<div class="_sPg">.*?<[/]div>',content)
    if len(summary) is not 0:
        return (html_to_text(summary[0]))
    summary=re.findall('<div class="_o0d">.*<[/]div>',content)
    if len(summary) is not 0:
        return (html_to_text(summary[0]))
    summary=re.findall('[(noun)(adverb)(verb)(adjective)]<[/]div><ol.*?<[/]li',content)
    response = ""
    for i in range(len(summary)):    
        response+=' ' +summary[i]
    if len(summary) is not 0:
        return (html_to_text(response)[1:])
    return(None)
        
def get_google_answer(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text
    #print(content)
        
    answer=re.findall('<div class="_XWk">.*?<[/]div>',content)       #E.g. Who is the president of India
    answer2=re.findall('<div class="_Tfc _j0k">.*?<[/]div>',content) #How fast is a cheetah?

    if len(answer) > 0:
        if len(answer2) > 0:
            return (html_to_text(answer[0])+' '+html_to_text(answer2[0]))
        return (html_to_text(answer[0]))
    
    answer=re.findall('<span class="_m3b".*?<[/]span>',content)  #calculator
    if len(answer) > 0:
        answers=""
        for ans in answer:
            answers+=html_to_text(ans)
        return answers 
    
    answer=re.findall('<div class="kltat">.*?<[/]div>',content)       #what is the longest river in the world
    answer2=re.findall('<div class="ellip klmeta">.*?<[/]div>',content)
    
    if len(answer) > 0:
        if len(answer2) > 0:
            return (html_to_text(answer[0])+' '+html_to_text(answer2[0]))
        return (html_to_text(answer[0]))
        
    answer=re.findall('<span class="cwcot".*?<[/]span>',content)  
    
    if len(answer) > 0:
        return (html_to_text(answer[0]))
        
    answer=re.findall('<span class="nobr"><h2 class="r".*?<[/]span>',content)  
    if len(answer) > 0:
        return (html_to_text(answer[0]))
        
    answer=re.findall('<span class="_G0d">.*?<[/]span>',content)  
    if len(answer) > 0:
        answers=""
        for ans in answer:
            answers+=html_to_text(ans)
        return answers
        
    answer=re.findall('<td style="font-size:16px">.*?<[/]td>',content)  
    if len(answer) > 0:
        return (html_to_text(answer[0]))
    
    return None

def get_google_answer2(question):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    # header variable
    headers = { 'User-Agent' : user_agent }
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url,headers=headers)
    content = r.text
    #print(content)
        
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
    
def get_google_correction(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text
    print content
    correction=re.findall('<a class="spell".*?<[/]a>',content)
    if len(correction)>0:
        return html_to_text(correction[0])
    return None

def get_google_questions(question):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    # header variable
    headers = { 'User-Agent' : user_agent }
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url,headers=headers)
    content = r.text.encode('UTF-8')
    questions=re.findall('<div class="_rhf">.*?<[/]div>',content)
    return [(html_to_text(q)) for q in questions]
    
def get_google_citeations(question):
    question=question.replace('+','%2B')
    url = 'https://www.google.co.in/search?q='+question.replace(' ','+')
    r = requests.get(url)
    content = r.text
    cites=re.findall('<cite>.*?<[/]cite>',content)
    urls =[]
    for cite in cites:
        text = html_to_text(cite)
        if text.startswith('https://') or text.startswith('www.'):
            urls.append(text)
    return urls

print(get_google_answer("shakespeare brother"))
