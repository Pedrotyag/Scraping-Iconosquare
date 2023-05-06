from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import os, platform
import time

import psw

#import traceback

class scraping:
    def __init__(self, path = 'Exist'):
        
        self.driver = None
        
        if(path == 'Exist'):
            self.path = os.getcwd() + os.sep + 'chromedriver.exe'
        else:
            self.path = path
    
    def oper_driver(self):


        if(platform.system() == 'Windows'):
            s = Service(self.path)
            driver = webdriver.Chrome(service=s)
            
            self.driver = driver

        else:

            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = psw.GOOGLE_CHROME_BIN
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument('--window-size=1920x1080')

            self.driver = webdriver.Chrome(executable_path = psw.CHROMEDRIVER_PATH, chrome_options=chrome_options)
        
        return self.driver
    
    def login(self, user_pass, password_pass):
        
        print("Login...")

        print(f"https://www.instagram.com/")

        self.driver.get(f"https://www.instagram.com/")

        username = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[name='username']")))
                                   
        password = self.driver.find_element(By.CSS_SELECTOR, "input[name='password']")

        username.clear()
        password.clear()
        username.send_keys(user_pass)
        password.send_keys(password_pass)

        login = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        time.sleep(15)

        print("Logado !!!")


    def to_user(self, username):

        self.driver.get(f"https://instagram.com/{username}")

        time.sleep(10)


        self.followers_number = WebDriverWait(self.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, '//a[@href="/eusouamom/followers/"]/span')))

        self.following_number = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@href="/eusouamom/following/"]/span/span')))

        self.publications_number = self.driver.find_element(By.XPATH, f'//span[@class="{self.followers_number.get_attribute("class")}"][1]')


        #----------------------------------------------------------------
        self.followers_number = self.followers_number.get_attribute("title")
        self.following_number = self.following_number.text
        self.publications_number = self.publications_number.text

        print(self.followers_number, self.following_number, self.publications_number)

        print(int([i if i.isdigit() else '' for i in self.followers_number]), int([i if i.isdigit() else '' for i in self.following_number]), int([i if i.isdigit() else '' for i in self.publications_number]))

        time.sleep(30)

    def test(self):

        print(f"https://www.google.com.br")

        self.driver.get(f"https://www.google.com.br")

        time.sleep(3)

        t = self.driver.find_element(By.XPATH, '//div[@class="FPdoLc lJ9FBc"]/center')

        t2 = t.find_element(By.XPATH, './/input[@class="gNO89b"]').get_attribute("aria-label")

        print(t2)






# Insta_scrape = scraping()
# Insta_scrape.oper_driver()
# #Insta_scrape.test()

# Insta_scrape.login("gda.bot.9@gmail.com", "GdA@Bot92023_2")
# #Insta_scrape.login("rosana.batata", "#0,2000SC")


# Insta_scrape.to_user("eusouamom")

