#example from https://selenium-python.readthedocs.io/getting-started.html

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
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome()

    #def setUp(self):

    def test_click_dynamic(self, url):
        self.driver.get(url)
        
        assert "dropdown" in self.driver.title
        
        menu = self.driver.find_element_by_class_name("dropbtn")
        hidden_submenu = self.driver.find_element_by_id("submenu1")

        actions = ActionChains(self.driver)
        actions.move_to_element(menu)
        actions.click(hidden_submenu)
       
        actions.perform()

    def test_click_static(self, url):
        self.driver.get(url)
        
        assert "dropdown" in self.driver.title
        
        menu = self.driver.find_element_by_class_name("menu")
        menu_item = self.driver.find_element_by_id("submenu1")

        actions = ActionChains(self.driver)
        actions.move_to_element(menu)
        actions.click(menu_item)
       
        actions.perform()
        
'''
    def test_runner(self, testLength):
        tmCurrentTime = time.time()
        tmStartTime = time.time()
        while (tmCurrentTime - testLength < tmStartTime):
            self.test_click("http://192.168.1.79/dropdown/dropdown_dynamic.html")
            tmCurrentTime = time.time()
        self.tearDown()
'''
    def tearDown(self):
        self.driver.close()
        #self.driver.quit()

fileName = 'data/selenium-'+str(datetime.date.today())+'-'+str(int(time.time()))+'.csv' 

dataDF = pd.DataFrame(columns=['task','time'])


if (len(sys.argv) > 1):
    testTime = float(sys.argv[1])
else: 
    testTime = 5 #default 5 seconds

#Dropdown button test
SolarServer = SolarServerTest()
dataDF = dataDF.append({'task' : 'start dynamic' , 'time': time.time()},ignore_index=True)

tmCurrentTime = time.time()
tmStartTime = time.time()
    
while (tmCurrentTime - testTime < tmStartTime):
    dataDF = dataDF.append({'task' : 'click' , 'time': time.time()},ignore_index=True)
    SolarServer.test_click_dynamic("http://192.168.1.79/dropdown/dropdown_dynamic.html")
    tmCurrentTime = time.time()

SolarServer.tearDown()
dataDF = dataDF.append({'task' : 'stop dynamic' , 'time': time.time()},ignore_index=True)

time.sleep(10)

# Static button test
SolarServer = SolarServerTest()
dataDF = dataDF.append({'task' : 'start static' , 'time': time.time()},ignore_index=True)

tmCurrentTime = time.time()
tmStartTime = time.time()
    
while (tmCurrentTime - testTime < tmStartTime):
    dataDF = dataDF.append({'task' : 'click' , 'time': time.time()},ignore_index=True)
    SolarServer.test_click_static("http://192.168.1.79/dropdown/dropdown_static.html")
    tmCurrentTime = time.time()

SolarServer.tearDown()
dataDF = dataDF.append({'task' : 'stop static' , 'time': time.time()},ignore_index=True)


#save data to file
# check if the file already exists
try:
    with open(fileName) as csvfile:
        print("This file already exists!")
except:
    dataDF.to_csv(fileName, sep=',',index=False)

print(dataDF)