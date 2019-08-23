#example from https://selenium-python.readthedocs.io/getting-started.html

from selenium import webdriver
from selenium.webdriver import ActionChains
import time

class SolarServerTest:
    
    def __init__(self):
        print time.time()
        self.driver = webdriver.Firefox()
        #self.driver = webdriver.Chrome()

    #def setUp(self):

    def test_click(self, url):
        self.driver.get(url)
        assert "dropdown" in self.driver.title
        print time.time()
        #elem = driver.find_element_by_id("yesterday")
        #cookieMonster = driver.get_cookies()

        menu = self.driver.find_element_by_class_name("dropbtn")
        hidden_submenu = self.driver.find_element_by_id("submenu1")

        actions = ActionChains(self.driver)
        actions.move_to_element(menu)
        actions.click(hidden_submenu)
        print time.time()
        actions.perform()
        print time.time()

    def test_runner(self, testLength):
        tmCurrentTime = time.time()
        tmStartTime = time.time()
        while (True):#(tmCurrentTime - testLength < tmStartTime):
            self.test_click()
            self.tearDown()

    def tearDown(self):
        self.driver.close()
        #self.driver.quit()

SolarServer = SolarServerTest()

while (True):
    time.sleep(1)
    

    SolarServer.test_click("http://192.168.1.79/dropdown/dropdown_dynamic.html")
    SolarServer.tearDown()

