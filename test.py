import os
import time
import random
import sys
import re
import json
from datetime import datetime
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException,NoSuchElementException
from bs4 import BeautifulSoup
from time import sleep
from operator import itemgetter
flag = False
# Chromeのオプション設定
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
button_count = 1
image_list = []
userDATA = []
data = ""
# Chromeのメイン部分
chrome = webdriver.Chrome('./chromedriver',chrome_options=chrome_options)
# ウィンドウ最大化
chrome.maximize_window()
chrome.get("https://tinder.com/app/login")
WebDriverWait(chrome, 10).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[4]/div[1]/h1')))
WebDriverWait(chrome, 20).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="modal-manager"]/div/div')))
try:
    chrome.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button').click()
except NoSuchElementException:
    print('Error')
WebDriverWait(chrome, 10).until(lambda d: len(d.window_handles) > 1)

def operateScreen():
    global flag
    global image_list
    global userDATA
    image_list = []
    tag = ""
    introdaction = ""
    userName = ""
    if (flag == False):
        time.sleep(2)
    # tinderのプロフィールを表示
    chrome.find_element_by_tag_name("body").send_keys(Keys.UP)
    time.sleep(0.5)
    userName = chrome.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]').text
    
    try:
        tag = chrome.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]').text
    except NoSuchElementException:
        print('')
        
    try:
        introdaction = chrome.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]').text
    except NoSuchElementException:
        print('')
        
    userDATA.append(userName.replace('\n', ' '))
    userDATA.append(tag.replace('\n', ''))
    userDATA.append(introdaction.replace('\n', ''))
    for i in range(1,button_count):
        chrome.find_element_by_tag_name("body").send_keys(Keys.SPACE)
        time.sleep(0.5)
    data= chrome.execute_script("return window.performance.getEntriesByType('resource')")
    for i in data:
        if(i["initiatorType"] == 'img'):
            imag_url = i['name']
            matchOB = re.match(r"https://images-ssl.gotinder.com/",imag_url)
            if matchOB:
                image_list.append(imag_url)
                
def wrtiteJSON():
    global image_list
    global userDATA
    nums = int(button_count) * -1
    image_list = image_list[nums:]
    s = {'userinfo':userDATA,'imageLIST':image_list}
    d = json.dumps(s,ensure_ascii=False)
    print(d)
    dt = datetime.now().strftime("%Y%m%d%H%M%S")
    with open('./user/'+str(dt)+'.json', 'w') as f:
        json.dump(d, f,ensure_ascii=False)
        
    for i in image_list:
        fileName = i.split('/')[-1]
#        try:
#            with urllib.request.urlopen(i) as web_file:
#                data = web_file.read()
#                with open("./images/{0}".format(fileName), mode='wb') as local_file:
#                    local_file.write(data)
#        except urllib.error.URLError as e:
#            print(e)
    image_list = []
    userDATA = []
# ウィンドウの配列を格納
handle_array = chrome.window_handles
# Fasebookウィンドウに切り替え
chrome.switch_to.window(handle_array[1])
chrome.find_element_by_xpath('//*[@id="email"]').send_keys('railgan.love@gmail.com')
chrome.find_element_by_xpath('//*[@id="pass"]').send_keys('daiki1230')
chrome.find_element_by_xpath('//*[@id="u_0_0"]').click()

# Tinder画面に切りかえ
chrome.switch_to.window(handle_array[0])

def reloadDATA():
    WebDriverWait(chrome, 8).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]')))
    data= chrome.execute_script("return window.performance.getEntriesByType('resource')")



#WebDriverWait(chrome, 20).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]')))
data= chrome.execute_script("return window.performance.getEntriesByType('resource')")

try:
    WebDriverWait(chrome, 4).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]')))
    UserTables = chrome.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]')
    print(UserTables.text)
    button_count = int(str(UserTables.text).replace('\n', '')[-1])
    operateScreen()
    wrtiteJSON()
except TimeoutException:
    print('Error')
    operateScreen()
    wrtiteJSON()
chrome.find_element_by_tag_name("body").send_keys(Keys.LEFT)
    
   
   
val = input('ログイン後、0を押してください')
max_count = 500
print(type(val))
if val == "0":
    flag = True
    for num in range(1,max_count):
        image_list = []
        userDATA = []
        print('image_list:',image_list)
        print('userDATA:',userDATA)
        num=num+1
        reloadDATA()
        try:
            WebDriverWait(chrome, 2).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]')))
            UserTables = chrome.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]')
            print(UserTables.text)
            button_count = int(str(UserTables.text).replace('\n', '')[-1])
            operateScreen()
            wrtiteJSON()
        except TimeoutException:
            print('Error')
            button_count = 1
            operateScreen()
            wrtiteJSON()
            
        chrome.find_element_by_tag_name("body").send_keys(Keys.LEFT)
        time.sleep(0.3)
            
        print(str(num))
    print(str(max_count)+"人スワイプしました")
    chrome.close()
    
    