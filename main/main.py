from selenium import webdriver
from selenium.webdriver.common.by import By

#config
user = "MateuszL"
password = "Qw1atek1"
link = "https://sio2.staszic.waw.pl/"
point_threshold = 0
dir = "C:\\Users\\jarek\\Documents"
##########


#configuring the driver
browser = webdriver.Edge()
browser.implicitly_wait(2)

#searching for login
browser.get(link+"\login\\")
login_name = browser.find_element(By.ID, "id_username")
login_password = browser.find_element(By.ID, "id_password")
login_button = browser.find_element(By.CLASS_NAME, "btn btn-primary g-recaptcha")

login_name.send_keys(user)
login_password.send_keys(password)
login_button.click()
