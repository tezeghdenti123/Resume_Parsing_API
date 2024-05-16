from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import chromedriver_autoinstaller
from selenium import webdriver
from Models.Opportunite import Opportunite
from flask import jsonify
import time
from Services.MySqlService import MySqlService
import re
import csv
import threading
import schedule

class ScrapingService:
    def getDriver(self):
        opt = webdriver.ChromeOptions()
        opt.add_argument("--start-maximized")

        chromedriver_autoinstaller.install()
        driver = webdriver.Chrome(options=opt)
        return driver
    def signIn(self,driver):
        driver.get("https://www.turnover-it.com/#login_modal")
        time.sleep(5)
        email="Tezeghdent"
        password="Medmarbac2019$"
        email_input=driver.find_elements(By.NAME,"username")
        email_input[0].send_keys(email)
        password_input=driver.find_elements(By.NAME,"password")
        password_input[0].send_keys(password)
        button=driver.find_elements(By.NAME,"login")
        button[0].click()

        
    def getListOfOpportunite(self,driver):
        titles_list=[]
        description_list=[]
        contracts_details=[]
        locations_list=[]
        page_index=str(1)
        i=1
        wait_time=40
        while True:
            try:

                # Find the target element
                target_element = WebDriverWait(driver, wait_time).until(EC.element_to_be_clickable((By.XPATH, "//a[contains(@onclick, 'pagetri("+page_index+"')]")))
                time.sleep(10)
                target_element.click()
                time.sleep(10)
                # Scroll to the element to ensure it's in view
                #driver.execute_script("arguments[0].scrollIntoView(true);", target_element)
                # Use ActionChains to click on the element using JavaScript
                #ActionChains(driver).move_to_element(target_element).click().perform()
                title_list_element= WebDriverWait(driver, wait_time).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "textbleu11bold")))
                #title_list_element=driver.find_elements(By.CLASS_NAME,"textbleu11bold")
                description_list_element = WebDriverWait(driver, wait_time).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "textnoir9")))        #description_list_element=driver.find_elements(By.CLASS_NAME,"textnoir9")
                description_list_element=description_list_element[1:]
                contracts_detail_element=description_list_element[1::2]
                description_list_element=description_list_element[0::2]
                location_list_element= WebDriverWait(driver, wait_time).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "textgrisfonce9")))
                #location_list_element=driver.find_elements(By.CLASS_NAME,"textgrisfonce9")

                print(title_list_element[0].text)
                for j in range(len(title_list_element)):
                    titles_list.append(title_list_element[j].text)
                    description_list.append(description_list_element[j].text)
                    contracts_details.append(contracts_detail_element[j].text)
                    locations_list.append(location_list_element[j].text)

                i+=1
                page_index=str(i)

            except TimeoutException as e:
                print("TimeoutException: Internet connection!")
                return [titles_list,description_list,contracts_details,locations_list]
            except Exception as e:
                print("TimeoutException: Internet connection!")
                return [titles_list,description_list,contracts_details,locations_list]


    def getCleanedOpportunityList(self,mysql,app):
        with app.app_context():
            driver=self.getDriver()
            #driver.get("https://google.com")
            self.signIn(driver)
            driver.get("https://www.turnover-it.com/livedemandes")
            listOpportunité=self.getListOfOpportunite(driver)
            titles_list=listOpportunité[0]
            description_list=listOpportunité[1]
            contracts_details=listOpportunité[2]
            locations_list=listOpportunité[3]
            table=[
            ["titre","description","date_deposition","tjm","durée","location"]
            ]
            mysqlService=MySqlService()
            mysqlService.deleteAllOpportunity(mysql)
            for i in range(len(titles_list)):
                auxList=[]
                auxList.append(titles_list[i])
                auxList.append(description_list[i])
                aux=contracts_details[i].split('|')
                auxList.append(aux[0])
                auxList.append(aux[1])
                auxList.append(aux[2])
                auxList.append(locations_list[i])
                opportunite=Opportunite(auxList[0],auxList[1],auxList[2],auxList[3],auxList[4],auxList[5])
                tjm=int(self.extract_numbers(auxList[3]))
                
                mysqlService.saveOpportunity(mysql,auxList[0],auxList[1],auxList[2],tjm,auxList[4],auxList[5])
                table.append(opportunite.__dict__)
            return jsonify(table)
        '''with app.app_context():
            print("run")
            mysqlService=MySqlService()
            mysqlService.saveOpportunity(mysql,"test","test","test","test","test","test")
            print("runed")'''

    '''def schedule_scraping_task(self,mysql):
        schedule.every(1).minutes.do(self.getCleanedOpportunityList,args=[mysql])
        while True:
            schedule.run_pending()
            time.sleep(1)'''
    def extract_numbers(self,input_string):
        # Regular expression to match numbers
        pattern = r'\d+'
        # Find all matches of the pattern in the input string
        numbers = re.findall(pattern, input_string)
        # Join the matched numbers into a single string
        result = ''.join(numbers)
        return result
    
   
