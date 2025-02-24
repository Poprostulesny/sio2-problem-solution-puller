from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.relative_locator import locate_with
from selenium.common.exceptions import NoSuchElementException
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
    
    tasks_links = []
    t=1
    pom=[]

    for i in links:
        if(t<len(tasks_subjects)):
            if i.location['y']<tasks_subjects[t].location['y']:
                pom.append({
                "text": i.text,
                "href": i.get_attribute("href")
                })
            else:
                tasks_links.append([tasks_subjects[t-1].text,pom])
                pom=[]
                t+=1
                pom.append({
                "text": i.text,
                "href": i.get_attribute("href")
                })
        else:
            pom.append({
            "text": i.text,
            "href": i.get_attribute("href")
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

    
