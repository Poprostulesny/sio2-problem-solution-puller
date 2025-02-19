from selenium import webdriver
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.relative_locator import locate_with
import time
import utils
from collections import ChainMap
#config
user = "MateuszL"
password = "Qw1atek1"
link = "https://sio2.staszic.waw.pl/"
point_threshold = 0
dir = "C:\\Users\\jarek\\Documents"
##########


#configuring the driver
browser = webdriver.Edge()
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

choice = int(input())
print("You chose ", list_of_options[choice].text, " . \nPress Y if you want to continue." )

p=input()
if p != 'Y' and p != 'y':
    quit()

###################
# We're in
list_of_options[choice].click()

#getting to tasks
url = browser.current_url
url= utils.redirect_to_tasks(url)
browser.get(url)

#getting the tasks
#we need to do it for every site of tasks
#then merge the results
tasks_subjects = browser.find_elements(By.CLASS_NAME,"problemlist-subheader")
tasks = []
for i in range(len(tasks_subjects)):
   
    if i == len(tasks_subjects)-1:
        pom=browser.find_elements(locate_with(By.TAG_NAME,"a").below(tasks_subjects[i]).above(tasks_subjects[i+1]))
    else:
        pom=browser.find_elements(locate_with(By.TAG_NAME,"a").below(tasks_subjects[i]).above({By.TAG_NAME: "footer"}))
    
    tasks.append([tasks_subjects[i].text, pom_links, pom_files, pom_names])






time.sleep(5)
