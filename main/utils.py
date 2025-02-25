from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import NoSuchElementException
from functools import cmp_to_key
import time
import os

def get_base_url(url):
    desc_iter=0
    for i in range(len(url)-1):
        desc_iter = len(url)-i-2
        if(url[desc_iter]=='/'):
            break
    url_new =""
    for i in range(desc_iter):
        url_new=url_new + url[i]
    return url_new

def redirect_to_tasks(url):
    url_new = get_base_url(url)
    url_new+="/p"
    return(url_new)

def redirect_to_solutions(url):
    url_new = get_base_url(url)
    url_new+="/submissions"
    return(url_new)

def how_many_pages(browser:webdriver.Edge):
    try:
        page = browser.find_element(By.CLASS_NAME,"pagination")
        links = page.find_elements(By.TAG_NAME,"a")
        return len(links)-2
    except NoSuchElementException:
        return 1

def extract_link_structure(pages, browser:webdriver.Edge):
    if(pages == 1):
        return link_structure([], browser)
    else:
        tasks_links_tab = []
        base_url = get_base_url(browser.current_url)+"/p"
        for i in range(pages):
            browser.get(base_url+"/?page=" + str(i+1))
            tasks_links_tab = link_structure(tasks_links_tab, browser)
    return tasks_links_tab
    


        
def link_structure(tasks_links_old, browser:webdriver.Edge):
    parent_div = browser.find_element(By.CLASS_NAME, "table")
    #getting the div
    tasks_subjects= parent_div.find_elements(By.CLASS_NAME,"problemlist-subheader")
    links=parent_div.find_elements(By.TAG_NAME,"a")
    id = browser.find_elements(locate_with(By.TAG_NAME,"td").to_left_of(links[0]))
    tasks_links = []
    t=1
    pom=[]
    
   
    for i in range(len(links)):
        if(t<len(tasks_subjects)):
            if links[i].location['y']<tasks_subjects[t].location['y']:
                pom.append({
                "text": links[i].text,
                "href": links[i].get_attribute("href"),
                "id": id[i].text
                })
            else:
                tasks_links.append([tasks_subjects[t-1].text,pom])
                pom=[]
                t+=1
                pom.append({
                "text": links[i].text,
                "href": links[i].get_attribute("href"),
                 "id": id[i].text
                })
        else:
            pom.append({
            "text": links[i].text,
            "href": links[i].get_attribute("href"),
             "id": id[i].text
            })

    tasks_links.append([tasks_subjects[len(tasks_subjects)-1].text,pom])   

    if len(tasks_links_old)==0:
        return tasks_links
    
    else:
        if(tasks_links_old[len(tasks_links_old)-1][0] == tasks_links[0][0]):
           tasks_links_old[len(tasks_links_old)-1][1].extend(tasks_links[0][1])
           tasks_links.pop(0)

        tasks_links_old.extend(tasks_links)
            
    return tasks_links_old


def print_link_structure(link_structure):
    for i in link_structure:
        print(i[0].upper())
        for y in i[1]:
            print(y)
            
#link_structure structure - (topic,list_of_tasks[{"text", "href", "id"}])
def create_map(link_structure):
    dictionary = dict()
    for i in range(len(link_structure)):
        for y in range(len(link_structure[i][1])):
            dictionary[link_structure[i][1][y]["id"]]=[i,y]
    return dictionary

    
def extract_result_structure(pages, browser: webdriver.Edge):
    #results = ("id", "score", "link")
    results= []
    base_url = get_base_url(browser.current_url) +"/submissions/"
    if(pages == 1):
        browser.get(base_url)
        return result_structure(results, browser)
    
    for i in range(pages):
        browser.get(base_url+"/?page=" + str(i+1))
        results = result_structure(browser, results)
    return results

def id_from_name(str):
    i=0
    id = "" 
    while str[i]!= '(':
        i+=1

    i+=1

    while str[i]!= ')':
        id= id + str[i]
        i+=1
    return id

def result_structure(browser:webdriver.Edge, result_structure_old):
    #browser.get("https://sio2.staszic.waw.pl/c/matinf_k20_c/submissions/")
    #szukamy elementów ze zgłoszeń poniżęj rubryki wynik i na prawo od rubryki status - same wyniki
    zgloszenia = browser.find_element(By.XPATH,"//*[contains(text(), 'Status')]")
    wynik = browser.find_element(By.XPATH,"//*[contains(text(), 'Wynik')]")
    rodzaj = browser.find_element(By.XPATH,"//*[contains(text(), 'Rodzaj')]")
    zadania = browser.find_element(By.XPATH,"//*[contains(text(), 'Zadanie')]")
    czas = browser.find_element(By.XPATH,"//*[contains(text(), 'Czas zgłoszenia')]")
    margines = browser.find_element(By.CLASS_NAME,"submission__margin")
    score = browser.find_elements(locate_with(By.TAG_NAME,'td').below(wynik).to_right_of(zgloszenia))
    tasks = browser.find_elements(locate_with(By.TAG_NAME,'td').below(zadania).to_right_of(czas).to_left_of(rodzaj))
    links = browser.find_elements(locate_with(By.TAG_NAME,'a').below(czas).to_left_of(zadania).to_right_of(margines))
    
    for i in range(len(tasks)):
        if(score[i].text == ''):
            result_structure_old.append({ "id":id_from_name(tasks[i].text), "score": 0, "link" :links[i].get_attribute("href")})
        else:
            result_structure_old.append({ "id":id_from_name(tasks[i].text), "score": int(score[i].text), "link" :links[i].get_attribute("href")})
    
    return result_structure_old

def comp(a, b):
    if a["id"]==b["id"]:
        if(a["score"]<b["score"]):
            return -1
        elif a["score"]==b["score"]:
            return 0
        else:
            return 1
    elif(a["id"]<b["id"]):
        return -1
    else:
        return 1
   
def only_best_results(results):
    results.sort(key = cmp_to_key(comp))
    new = []
    for i in range(len(results)-1):
        if(results[i]["id"]!=results[i+1]["id"]):
            new.append(results[i])
    new.append(results[len(results)-1])
    return new

def match_to_map(results, dict, links, browser:webdriver.Edge):
    for x in results:
        i, y = dict[x["id"]]
        links[i][1][y]["score"]=x["score"]
        links[i][1][y]["sol_link"]=x["link"]+"download/"
    return links
        
# def create_filesystem:
        