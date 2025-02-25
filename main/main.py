from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.relative_locator import locate_with
import time
from collections import ChainMap
import os
import utils
import config

#config
user, password, link, dir = config.fileconfig()
point_threshold = 0
##########

#configuring the driver
dir_temp = dir + "\\temp"
options = webdriver.EdgeOptions()
#options.add_argument("--headless")
options.add_argument("--print-to-pdf")#enable printing
options.add_argument("--kiosk-printing")#disable prompt
prefs = {"printing.print_preview_sticky_settings.appState": '{"recentDestinations":[{"id":"Save as PDF","origin":"local","account":"","capabilities":{}}],"selectedDestinationId":"Save as PDF","version":2}',"savefile.default_directory":dir_temp}
options.add_experimental_option("prefs", prefs)
browser = webdriver.Edge(options=options)
browser.implicitly_wait(4)


#searching for login
browser.get(link+"\\login\\")
login_name = browser.find_element(By.ID, "id_username")
login_password = browser.find_element(By.ID, "id_password")
login_button = browser.find_element(locate_with(By.TAG_NAME,"button").below({By.ID: "id_password"}))

#logging in
login_name.send_keys(user)
login_password.send_keys(password)
login_button.click()

#asking the user which contest do they want to pull from
table = browser.find_elements(By.CLASS_NAME, "toggle-cg")
list_of_options = []
for i in range(len(table)):
    table[i].click()
    if(i!=len(table)-1):
        pom=browser.find_elements(locate_with(By.TAG_NAME,"a").below(table[i]).above(table[i+1]))
    else:
        pom=browser.find_elements(locate_with(By.TAG_NAME,"a").below(table[i]).above({By.TAG_NAME: "footer"}))
    for t in pom:
        list_of_options.append(t)

print("Choose the number corresponding to the contest which answers you want to pull")
for i in range(len(list_of_options)):
    print(i,list_of_options[i].text)

#choice = int(input())
choice =0
print("You chose ", list_of_options[choice].text, " . \nPress Y if you want to continue." )

#p=input()
p='y'
if p != 'Y' and p != 'y':
    quit()

###################
# We're in
list_of_options[choice].click()

#getting to tasks
url_base = browser.current_url
url= utils.redirect_to_tasks(url_base)
browser.get(url)
pages = utils.how_many_pages(browser)

#extracting link structure
#link_structure structure - (topic,list_of_tasks[{"text", "href", "id"}])
#link_structure = utils.extract_link_structure(pages,browser)

#dictionary = utils.create_map(link_structure)


url= utils.redirect_to_solutions(url_base)
browser.get(url)
pages = utils.how_many_pages(browser)
#result_structure = ("id", "score", "link")

result_structure = utils.extract_result_structure(pages, browser)

result_structure = utils.only_best_results(result_structure)
for i in result_structure:
    print(i)
    

# browser.get("https://sio2.mimuw.edu.pl/c/oi32-1/p/bit/")
# browser.execute_script('window.print();')
# time.sleep(5)





time.sleep(5)
