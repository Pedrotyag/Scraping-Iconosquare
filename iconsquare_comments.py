from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

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

        self.url_login = 'https://app.iconosquare.com/signin'
    
    def oper_driver(self):


        if(platform.system() == 'Windows'):
            s = Service(self.path)

            chrome_options = webdriver.ChromeOptions()
            prefs = {"download.default_directory" : os.path.dirname(os.path.realpath(__file__))}
            chrome_options.add_experimental_option("prefs", prefs)
            
            driver = webdriver.Chrome(service=s, chrome_options=chrome_options)
            
            self.driver = driver

            print("Rodando no windows...")

        else:

            chrome_options = webdriver.ChromeOptions()
            chrome_options.binary_location = psw.GOOGLE_CHROME_BIN
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument('--window-size=1920x1080')

            prefs = {"download.default_directory" : os.path.dirname(os.path.realpath(__file__))}
            chrome_options.add_experimental_option("prefs",prefs)

            self.driver = webdriver.Chrome(executable_path = psw.CHROMEDRIVER_PATH, chrome_options=chrome_options)

            print("Rodando no linux...")
        
        return self.driver
    
    def login(self, user_pass, password_pass):

        print(f'\n' + '-'*8 + 'Fazendo Login'  + '-'*8 + '\n')

        
        print(f"Login... - {self.url_login}")

        self.driver.get(self.url_login)

        username = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))
                                   
        password = self.driver.find_element(By.XPATH, '//*[@id="password"]')

        username.clear()
        password.clear()
        username.send_keys(user_pass)
        password.send_keys(password_pass)

        login = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        overview = WebDriverWait(self.driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//h1[text()="Hello Amom!"]')))

        time.sleep(5)

        print("Logado !!!\n")


    def scroll_until_end_page(self):

        body = self.driver.find_element(By.XPATH, "/html/body")
        
        quant = 5

        print('\n' + '-'*8 + f'Scrolling [Total {quant}]'  + '-'*8 + '\n')

        i = 1
        while(i <= quant):
            if(i==quant):
                print(f'Scrolling... {i}\n')
            else:
                print(f'Scrolling... {i}')

            body.send_keys(Keys.CONTROL, Keys.END)
            i += 1
            time.sleep(3)
            
          
    def list_comments(self):

        print('\n' + '-'*8 + f'Listando os Posts'  + '-'*8 + '\n')

        overview = WebDriverWait(self.driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//h2[text()="Overview"]')))

        self.driver.get(f"https://app.iconosquare.com/content/posts")

        b1 = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper-logged"]/div[2]/div/div/div/div/div[1]/div[2]/div/div/button/div/div[3]/div/i'))).click()

        b2 = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper-logged"]/div[2]/div/div/div/div/div[1]/div[2]/div/div/div/ul/li[5]/button'))).click()

        b1 = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="wrapper-logged"]/div[2]/div/div/div/div/div[1]/div[2]/div/div/button/div/div[3]/div/i'))).click()

        self.scroll_until_end_page()

        time.sleep(3)

        self.all_comments_elements = self.driver.find_elements(By.XPATH, '//*[@id="wrapper-logged"]/div[2]/div/div/div/div/div[2]/div/main/div/div[2]/div/div[1]/div[1]')

        self.quant_posts_30_dias = len(self.all_comments_elements)

        print(f"Foram listados {self.quant_posts_30_dias} posts dos últimos 30 dias\n")

        return self.all_comments_elements
    
    def send_comments_to_email(self, email_address, list_comments, Email_manager):

        print('\n' + '-'*8 + f'Enviando os comentários via email'  + '-'*8 + '\n')
        
        self.links = []
        self.dates = []

        time_wait = 2
        for i in list_comments[23:]:

            i.click()

            time.sleep(time_wait)

            #------ Link, Data e Legenda ------
            
            self.link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(@href, "https://www.instagram") and @role="button"]'))).get_attribute("href")

            self.links.append(self.link)

            self.date = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//p[text()="eusouamom"][1]//ancestor::div[1]//p[contains(@class, "Gray")]'))).text
            
            self.dates.append(self.date)
            
            subject =  self.driver.find_elements(By.XPATH, '//p[@class="break-words inline"]')

            self.subject_text = ''
            for element in subject[:]:

                self.subject_text += element.text + '\n'
                
                try:

                    subelement = element.find_elements(By.XPATH, './/a')
                    if(len(subelement) == 0):
                        raise
                        
                    for subelement2 in subelement:

                        if(str(subelement2.get_attribute("href")) == ''):
                            raise

                        if('tags' in str(subelement2.get_attribute("href"))):
                            self.subject_text += "#" + str(subelement2.get_attribute("href").split("/")[-1])
                        else:
                            self.subject_text += str(subelement2.get_attribute("href").split("/")[-1]) + '\n'

                except:

                    pass  

                self.subject_text += '\n'
            
            #-----------------------------------

            b1 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@data-testid="Comments"]'))).click()
            
            donwload_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@aria-label="export xls" and @title="Export the comments of this post"]'))).click()
            
            
            change_email_button = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[contains(text(),"Choose a different mail address")]'))).click()
            
            
            email = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="email"]')))


            email.clear()
            email.send_keys(email_address)

            send_button = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//button[contains(text(),"Confirm")]'))).click()

            try:
                send_success = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, '//p[contains(text(), "Success")]')))

                print(f"Envio Feito ! - link = {self.link}\n")
            except:
                
                print(f"Deu algum erro no envio! - link {self.link}\n")
                raise


            t1 = time.time()

            cond = True
            while(cond):
                
                if(Email_manager.email_ids_list()):

                    Email_manager.list_links(Email_manager.mail, Email_manager.id_list)

                    Email_manager.read_list_comp(self.link, self.date, self.subject_text)
                
                    if(Email_manager.search_link(Email_manager.links, Email_manager.list_comp)):
                        cond = False

                if(time.time() - t1 >= 60*30):
                    raise

                time.sleep(30)



            if(not Email_manager.download_file(Email_manager.list_links_out)):
                raise  

            Email_manager.create_df_excel()

            #-----------------------------------------------------------------------------------
            # Import writer class from csv module
            from csv import writer

            # List that we want to add as a new row
            List = [Email_manager.list_links_out]

            # Open our existing CSV file in append mode
            # Create a file object for this file
            with open('link.csv', 'a') as f_object:

                # Pass this file object to csv.writer()
                # and get a writer object
                writer_object = writer(f_object)

                # Pass the list as an argument into
                # the writerow()
                writer_object.writerow(List)

                # Close the file object
                f_object.close()

            # if(list_comments.index(i) == 0):
            #     raise

            close_1 = self.driver.find_element(By.XPATH, '//button[contains(text(), "Close")]').click()


            close_2 = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Close"]'))).click()
            
    def followers(self, Email_manager):

        self.driver.get(f"https://app.iconosquare.com/analytics/overview")

        overview = WebDriverWait(self.driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//h2[text()="Overview"]')))

        calendar_1 = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//i[contains(@class, "icon-chevron-bottom")][1]'))).click()

        calendar_2 = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[text()="This year"]'))).click()

        
        download_op1 = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//button[@aria-label="Export"][1]'))).click()

        download_csv_link = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//a[@download="followers_history"]'))).click()

        time.sleep(5)
        Email_manager.create_df_csv("followers_history.csv")

    def close(self):

        print('\n' + '-'*8 + f'Deslogando a conta'  + '-'*8 + '\n')
        print("Deslogando...")

        self.driver.get(f"https://app.iconosquare.com/analytics/overview")

        overview = WebDriverWait(self.driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//h2[text()="Overview"]')))

        AF = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="AF"]'))).click()

        logout = WebDriverWait(self.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//span[text()="Logout"]'))).click()
    
        print('\n' + '-'*8 + f'Fechando o navegador'  + '-'*8 + '\n')
        print("Fechando...")

        time.sleep(5)

        self.driver.close()
    
    def test(self):

        self.driver.get(f"https://stackoverflow.com/questions/32391303/how-to-scroll-to-the-end-of-the-page-using-selenium-in-python")
        time.sleep(5)

        self.scroll_until_end_page()






# Insta_scrape = scraping()
# Insta_scrape.oper_driver()

# Insta_scrape.login("iconosquare@amomlins.com", "XHm%M6By8ML3")

# Insta_scrape.close()

# list_comments = Insta_scrape.list_comments()
# Insta_scrape.send_comments_to_email("ptiago1414@gmail.com", list_comments)

#Insta_scrape.test()