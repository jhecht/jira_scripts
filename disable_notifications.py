from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import getpass
import requests
import json
from pprint import pprint
import time

#username = raw_input('Enter your username: ')
#pw = getpass.getpass('Enter your password: ')
#credentials = (username, pw)
adminUsername = 'xxxxx'
adminPw = 'xxxxx'
credentials = ('xxxxx','xxxxx')

jira_base_url = 'https://jira'
login_url = jira_base_url + '/login.jsp'
admin_url = jira_base_url + '/secure/admin/ViewApplicationProperties.jspa'
scheme_url = jira_base_url + '/secure/project/SelectProjectScheme!default.jspa?projectId=' 

r = requests.get('https://jira/rest/api/2/project', auth=credentials)
data = json.loads(r.text)
#pprint(data[0])
projectList =  map(lambda d: (d['key'], d['id']), data)
#pprint(projectList)

#same as:
##i = 0
##projectList = []

##for element in data:
##  projectList.append(data[i]['projectCategory']['id'])
##  i += 1
##print projectList 

browser = webdriver.Firefox()

# login as general user
browser.get(login_url)
usernameField = browser.find_element_by_id('login-form-username')
usernameField.send_keys(adminUsername)
passwordField = browser.find_element_by_id('login-form-password')
passwordField.send_keys(adminPw)
browser.find_element_by_id('login-form-submit').send_keys(Keys.CONTROL, Keys.ALT, 's')

time.sleep(3)

# login as admin
browser.get(admin_url)
time.sleep(3)
passwordField = browser.find_element_by_id('login-form-authenticatePassword')
time.sleep(3)
passwordField.send_keys(adminPw)
browser.find_element_by_id('login-form-submit').send_keys(Keys.CONTROL, Keys.ALT, 's')
time.sleep(5)

# go to notification scheme for each project
for (key,id) in projectList:
  browser.get(scheme_url + id) 

  #browser.get(scheme_url + projectList[0][1])
  schemeIds = Select(browser.find_element_by_name('schemeIds'))
  #time.sleep(3)
  #print schemeIds.getFirstSelectedOption()
  time.sleep(3)
  
  print schemeIds.first_selected_option.text
  if schemeIds.first_selected_option.text != "None":
  #if schemeIds.first_selected_option.get_attribute("value")  != '':
  #if schemeIds.select_by_visible_text != 'None':
    schemeIds.select_by_visible_text('None')
    browser.find_element_by_id('associate_submit').send_keys(Keys.CONTROL, Keys.ALT, 's') 
  else:
    browser.find_element_by_id('cancelButton').send_keys(Keys.CONTROL, Keys.ALT, '`')
time.sleep(3)
#browser.close()
