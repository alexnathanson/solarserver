
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

    def test_click_dynamic(self, url):
        
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

    def test_click_static(self, url):
        '''
        print(self.driver.get_cookies())
        self.driver.delete_all_cookies();
        print(self.driver.application_cache)
        '''

        self.driver.get(url)
        
        assert "dropdown" in self.driver.title
        
        menuS = self.driver.find_element_by_class_name("menu")
        menu_itemS = self.driver.find_element_by_id("submenu1")

        actions = ActionChains(self.driver)
        actions.move_to_element(menuS)
        actions.click(menu_itemS)
       
        actions.perform()
        
        self.driver.implicitly_wait(2)

    def tearDown(self):
        self.driver.close()
        #self.driver.quit()

fileName = 'data/selenium-'+str(datetime.date.today())+'-'+str(int(time.time()))+'.csv' 
print (fileName)
print("")

dataDF = pd.DataFrame(columns=['task','time'])

if (len(sys.argv) > 1):
    testTime = float(sys.argv[1])
else: 
    testTime = 5 #default 5 seconds

# run the whole thing twice to account for start up weirdness
for i in list(range(2)):

    time.sleep(20)

    #Dropdown button test
    print ("Starting dynamic test!")

    SolarServer = SolarServerTest()
    dataDF = dataDF.append({'task' : 'start dynamic ' + str(i) , 'time': time.time()},ignore_index=True)

    tmCurrentTime = time.time()
    tmStartTime = time.time()
        
    while (tmCurrentTime - testTime < tmStartTime):
        dataDF = dataDF.append({'task' : 'click' , 'time': time.time()},ignore_index=True)
        SolarServer.test_click_dynamic("http://192.168.1.79/dropdown/dropdown_dynamic_image.html")
        tmCurrentTime = time.time()
        dataDF = dataDF.append({'task' : 'click' , 'time': time.time()},ignore_index=True)
        SolarServer.test_click_dynamic("http://192.168.1.79/dropdown/dropdown_dynamic_imageB.html")
        tmCurrentTime = time.time()

    SolarServer.tearDown()
    dataDF = dataDF.append({'task' : 'stop dynamic ' + str(i) , 'time': time.time()},ignore_index=True)

    #chill out between tests
    time.sleep(20)

    # Static button test

    print ("Starting static test!")

    SolarServer = SolarServerTest()
    dataDF = dataDF.append({'task' : 'start static '+ str(i), 'time': time.time()},ignore_index=True)

    tmCurrentTime = time.time()
    tmStartTime = time.time()
        
    while (tmCurrentTime - testTime < tmStartTime):
        dataDF = dataDF.append({'task' : 'click' , 'time': time.time()},ignore_index=True)
        SolarServer.test_click_static("http://192.168.1.79/dropdown/dropdown_static.html")
        tmCurrentTime = time.time()
        dataDF = dataDF.append({'task' : 'click' , 'time': time.time()},ignore_index=True)
        SolarServer.test_click_static("http://192.168.1.79/dropdown/dropdown_staticB.html")
        tmCurrentTime = time.time()

    SolarServer.tearDown()
    dataDF = dataDF.append({'task' : 'stop static '+ str(i) , 'time': time.time()},ignore_index=True)

#save data to file
# check if the file already exists
try:
    with open(fileName) as csvfile:
        print("This file already exists!")
except:
    dataDF.to_csv(fileName, sep=',',index=False)

print(dataDF)