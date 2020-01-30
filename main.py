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

class ChoromeClass():
    
    # コンストラクタ
    def __init__(self):
        self.chrome_options = self.SettingChrome
        self.chrome = self.ChromeSetup
        
    @property
    def getChorome(self):
        return self.chrome
    
    # 起動するChromeオプション設定
    @property
    def SettingChrome(self):
        prefs = {"profile.default_content_setting_values.notifications" : 2}
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("prefs",prefs)
        return chrome_options
    
    # 起動するChromeオブジェクトを作成
    @property
    def ChromeSetup(self):
        chrome = webdriver.Chrome('./chromedriver',chrome_options=self.chrome_options)
        chrome.maximize_window()
        return chrome

    
class TinderClass():
    # コンストラクタ
    def __init__(self):
        # ユーザー情報
        self.user = ""
        self.password = ""
        self.chrome = self.SettingChrome
        self.AddScreenflag = False
    
    # TinderLogin
    @property
    def Login(self):
        # tinderにログイン部分
        self.chrome.get("https://tinder.com/app/login")
        # モーダルウィンドウ検知部分
        WebDriverWait(self.chrome, 10).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div/div[4]/div[1]/h1')))
        WebDriverWait(self.chrome, 10).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="modal-manager"]/div/div')))
        try:
            self.chrome.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div/div/div[3]/div[2]/button').click()
        except NoSuchElementException:
            print('Error')
        WebDriverWait(self.chrome, 10).until(lambda d: len(d.window_handles) > 1)
        
        # ウィンドウの配列を格納
        handle_array = self.chrome.window_handles
        # Fasebookウィンドウに切り替え
        self.chrome.switch_to.window(handle_array[1])
        self.chrome.find_element_by_xpath('//*[@id="email"]').send_keys(self.user)
        self.chrome.find_element_by_xpath('//*[@id="pass"]').send_keys(self.password)
        self.chrome.find_element_by_xpath('//*[@id="u_0_0"]').click()
        
        # Tinder画面に切りかえ
        self.chrome.switch_to.window(handle_array[0])
    
    # ログイン後の画面チェックローディング中検出
    @property
    def ReadyCheck(self):
        self.WAITTIME = 20
        try:
            WebDriverWait(self.chrome, int(self.WAITTIME)).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[6]/div/div[1]/div')))
            return True
        except NoSuchElementException:
            return False
    
    # プロフィール画像をチェック(一枚の場合)
    @property
    def ImageProfileCheck(self):
        WebDriverWait(self.chrome,5).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div')))
        data = self.chrome.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[1]/div/div[1]/div/div')
        path = str(data.get_attribute("style")).replace('url("','').replace('");','')
        start =int(path.find('https'))
        end = int(path.find('.jpg'))+4
        return path[start:end]
    
    # プロフィール画像をチェック(複数の場合)
    @property
    def OtherImageCheck(self):
        image_list = []
        try:
            WebDriverWait(self.chrome, 0.5).until(expected_conditions.presence_of_element_located((By.XPATH,'//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]')))
            UserTables = self.chrome.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div/div[1]/div[3]/div[1]/div[2]')
            button_count = int(str(UserTables.text).replace('\n', '')[-1])
            print('選択タブ数:',button_count)
            self.chrome.find_element_by_tag_name("body").send_keys(Keys.UP)
            for i in range (1,button_count):
                self.chrome.find_element_by_tag_name("body").send_keys(Keys.SPACE)
                time.sleep(0.15)
                data = self.chrome.find_element_by_css_selector('.profileCard__slider__imgShadow .Z\(-1\)')
                path = str(data.get_attribute("style")).replace('url("','').replace('");','')
                start =int(path.find('https'))
                end = int(path.find('.jpg'))+4
                image_list.append(path[start:end])
            datas = self.chrome.find_elements_by_css_selector('.profileCard__slider__imgShadow .Z\(-1\)')
            for i in datas:
                path = str(i.get_attribute("style")).replace('url("','').replace('");','')
                start =int(path.find('https'))
                end = int(path.find('.jpg'))+4
                image_list.append(path[start:end])
#            image_list = self.DATARESOURSECheck
#            nums = (int(button_count) * -1 ) + 1
#            image_list = image_list[nums:]
            return image_list
        except TimeoutException:
            return True
    
    # Developer部分からresouseチェック(廃止予定)
    @property
    def DATARESOURSECheck(self):
        image_list = []
        data= self.chrome.execute_script("return window.performance.getEntriesByType('resource')")
        for i in data:
            if(i["initiatorType"] == 'img'):
                imag_url = i['name']
                matchOB = re.match(r"https://images-ssl.gotinder.com/",imag_url)
                if matchOB:
                    image_list.append(imag_url)
        return image_list
    
    # プロフィール情報を確認
    @property
    def Introduction(self):
        userDATA = []
        tag =""
        introdaction = ""
        userName = self.chrome.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[1]').text
        try:
            tag = self.chrome.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[1]/div/div[2]').text
        except NoSuchElementException:
            print('')

        try:
            introdaction = self.chrome.find_element_by_xpath('//*[@id="content"]/div/div[1]/div/main/div[1]/div/div/div[1]/div[1]/div/div[2]/div[2]').text
        except NoSuchElementException:
            print('')
            
        userDATA.append(userName.replace('\n', ' '))
        userDATA.append(tag.replace('\n', ' '))
        userDATA.append(introdaction.replace('\n', ' '))
        return userDATA
    
    # JSONに書き出すところ
    def JSONDump(self,data):
        dt = datetime.now().strftime("%Y%m%d%H%M%S")
        with open('./user/'+str(dt)+'.json', 'w') as f:
            json.dump(data, f,ensure_ascii=False)
        
    # Tinderクラスを管理するメイン部分
    def ManagementTinder(self,max_count):
        images = []
        userInfo = []
        self.Login
        if self.ReadyCheck:
            images.append(self.ImageProfileCheck)
            data = self.OtherImageCheck
            if( data != True):
                images.extend(data)
            images = list(set(images))
            userInfo = self.Introduction
        s = {'userinfo':userInfo,'imageLIST':images}
        d = json.dumps(s,ensure_ascii=False)
        self.JSONDump(d)
        self.chrome.find_element_by_tag_name("body").send_keys(Keys.LEFT)
        if (max_count == 0):
            return 0
        for num in range(1,max_count):
            images = []
            userInfo = []
            if self.AddScreenflag == False:
                time.sleep(1.5)
            try:
                print(self.chrome.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]').text)
                self.chrome.find_element_by_xpath('//*[@id="modal-manager"]/div/div/div[2]/button[2]/span').click()
                AddScreenflag = True
            except NoSuchElementException:
                print('')
            images.append(self.ImageProfileCheck)
            data = self.OtherImageCheck
            if( data != True):
                images.extend(data)
            images = list(set(images))
            userInfo = self.Introduction
            s = {'userinfo':userInfo,'imageLIST':images}
            d = json.dumps(s,ensure_ascii=False)
            self.JSONDump(d)
            self.chrome.find_element_by_tag_name("body").send_keys(Keys.LEFT)
            print(num)
            print('実画像数:',len(images))
        print(str(max_count)+"人スワイプしました")
            
            
    # Choromeオブジェクトの作成
    @property
    def SettingChrome(self):
        _chrome = ChoromeClass()
        return _chrome.getChorome


t = TinderClass()
t.ManagementTinder(500)