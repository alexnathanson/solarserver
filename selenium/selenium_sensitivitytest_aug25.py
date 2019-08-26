
from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import datetime
import numpy as np
import pandas as pd
import csv
import sys

class SolarServerTest:
    
    def __init__(self):
        #print time.time()
        #self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome()

        #need to avoid cache for accurate tests in some instances
        self.profile = webdriver.firefox.firefox_profile.FirefoxProfile()
        self.profile.set_preference("browser.cache.disk.enable", False)
        self.profile.set_preference("browser.cache.memory.enable", False)
        self.profile.set_preference("browser.cache.offline.enable", False)
        self.profile.set_preference("network.http.use-cache", False) 
        self.driver = webdriver.Firefox(self.profile)
        
    #def setUp(self):

    def test_click(self, url):
        
        '''
        print(self.driver.get_cookies())
        self.driver.delete_all_cookies();
        print(self.driver.application_cache)
        '''

        self.driver.get(url)

        assert "dropdown" in self.driver.title
        
        menu = self.driver.find_element_by_class_name("dropbtn")
        hidden_submenu = self.driver.find_element_by_id("submenu1")

        actions = ActionChains(self.driver)
        actions.move_to_element(menu)
        actions.click(hidden_submenu)
       
        actions.perform()

        self.driver.implicitly_wait(2)

    def test_singleload(self, url):

        #self.driver.implicitly_wait(10)

        self.driver.get(url)

        #assert "dropdown" in self.driver.title
        
    '''
    def test_click_static(self, url):
        
        #print(self.driver.get_cookies())
        #self.driver.delete_all_cookies();
        #print(self.driver.application_cache)
        

        self.driver.get(url)
        
        assert "dropdown" in self.driver.title
        
        menuS = self.driver.find_element_by_class_name("menu")
        menu_itemS = self.driver.find_element_by_id("submenu1")

        actions = ActionChains(self.driver)
        actions.move_to_element(menuS)
        actions.click(menu_itemS)
       
        actions.perform()
        
        self.driver.implicitly_wait(2)
    '''
    def tearDown(self):
        self.driver.close()
        #self.driver.quit()

fileName = 'data/selenium-sensitivity-'+str(datetime.date.today())+'-'+str(int(time.time()))+'.csv' 
print (fileName)
print("")

dataDF = pd.DataFrame(columns=['task','time'])

#60 seconds idle
time.sleep(60)


print ("Starting system sensitivity tests")

print("idle browser test")
dataDF = dataDF.append({'task' : 'start idle', 'time': time.time()},ignore_index=True)
SolarServer = SolarServerTest()
time.sleep(20)
SolarServer.tearDown()
dataDF = dataDF.append({'task' : 'stop idle', 'time': time.time()},ignore_index=True)

time.sleep(60)

print("one load browser test - blank html page")
dataDF = dataDF.append({'task' : 'start single load', 'time': time.time()},ignore_index=True)
SolarServer = SolarServerTest()
dataDF = dataDF.append({'task' : 'load' , 'time': time.time()},ignore_index=True)
SolarServer.test_singleload("http://192.168.1.79/dropdown/blank.html")
time.sleep(20)
SolarServer.tearDown()
dataDF = dataDF.append({'task' : 'stop single load', 'time': time.time()},ignore_index=True)

time.sleep(60)

print("one load browser test - large image")
dataDF = dataDF.append({'task' : 'start single load', 'time': time.time()},ignore_index=True)
SolarServer = SolarServerTest()
dataDF = dataDF.append({'task' : 'load' , 'time': time.time()},ignore_index=True)
SolarServer.test_singleload("http://192.168.1.79/dropdown/dropdown_dynamic_limageA.html")
time.sleep(20)
SolarServer.tearDown()
dataDF = dataDF.append({'task' : 'stop single load', 'time': time.time()},ignore_index=True)

time.sleep(60)


print("one load browser test - small image")
dataDF = dataDF.append({'task' : 'start single load', 'time': time.time()},ignore_index=True)
SolarServer = SolarServerTest()
dataDF = dataDF.append({'task' : 'load' , 'time': time.time()},ignore_index=True)
SolarServer.test_singleload("http://192.168.1.79/dropdown/dropdown_dynamic_simageA.html")
time.sleep(20)
SolarServer.tearDown()
dataDF = dataDF.append({'task' : 'stop single load', 'time': time.time()},ignore_index=True)

time.sleep(60)

   
#save data to file
# check if the file already exists
try:
    with open(fileName) as csvfile:
        print("This file already exists!")
except:
    dataDF.to_csv(fileName, sep=',',index=False)

print(dataDF)