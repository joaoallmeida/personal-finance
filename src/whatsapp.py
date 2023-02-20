from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
from dataclasses import dataclass
import time, logging, urllib

@dataclass
class Whatsapp:

    def _check_element_exists(self,driver:any ,by:any ,element:str) -> bool:
        try:
            driver.find_element(by,element)
        except NoSuchElementException:
            return False
        else:
            return True
        
    def send_message(self,phone_number:str, message:str) -> str:

        BASE_URL = "https://web.whatsapp.com/"
        MESSAGE_URL = f"https://web.whatsapp.com/send?phone={phone_number}&text={urllib.parse.quote(message)}"

        try:
            option = webdriver.ChromeOptions()

            option.add_argument('user-data-dir=/tmp/selenium/whatsappCokies')
            option.add_argument('--no-sandbox')
            option.add_argument('disable-extensions')
            option.add_argument('start-maximized')

            driver = webdriver.Remote(
                command_executor="http://chrome:4444",
                options=option
            )
            
            driver.get(BASE_URL)
            logging.info('Waiting 5 secs for page load.')
            time.sleep(5) # time for wait load page. 

            while self._check_element_exists(driver,By.ID,'side') == False:
                
                logging.info('Waiting to scan the QRcode.')
                time.sleep(3)

            else:
                logging.info('QRcode scanned, sending message.')

                driver.get(MESSAGE_URL)

                element  = WebDriverWait(driver,60).until(
                    EC.element_to_be_clickable((By.XPATH,'//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button'))
                    )
    
                element.click()
                logging.info('Message sent successfully')

        except Exception as e:
            raise e 
        else:
            logging.info('Closing execution.')
            time.sleep(3)
            driver.quit()