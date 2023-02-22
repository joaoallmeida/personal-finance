import time, logging, selenium.common.exceptions as ex
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from dataclasses import dataclass
from pathlib import Path
from typing import Union

@dataclass
class Bank:
    agency:str
    account:str
    password:str

    def _login(self, driver:any) -> None:
        logging.info('Logging into the account.')
        try:
            formAgency = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID, 'agencia'))).send_keys(self.agency)
            formAccount = driver.find_element(By.ID, 'conta').send_keys(self.account)
            buttonLogin = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div[2]/div/div[2]/div[2]/form/button[2]'))).click()

            for password in self.password:
                WebDriverWait(driver,10).until(
                    EC.element_to_be_clickable((By.XPATH,f'//*[@id="frmKey"]/fieldset/div[2]/div[1]/a[contains(text(),{password})]')
                )).click()
                time.sleep(1)

            driver.find_element(By.XPATH,'//*[@id="acessar"]').click()

        except Exception as e:
            logging.error(f'Failed to login in the account: {e}')
            raise e
        else:
            logging.info('Login completed successfully!')

    def _download_credit_invoice(self, driver:any) -> None:
        # # credit Card Page
        logging.info('Downloading credit card invoice.')
        try:
            creditCardAccordion = WebDriverWait(driver,10).until( EC.element_to_be_clickable((By.XPATH,'//*[@id="cartao-card-accordion"]/div[2]/voxel-icon/div/span'))).click()
            creditCardAccordionContent = WebDriverWait(driver,10).until( EC.element_to_be_clickable((By.XPATH,'//*[@id="content-cartao-card-accordion"]/div[1]/table/tbody/tr/td[1]/div/div[1]/a'))).click()
            buttonInvoices = WebDriverWait(driver,10).until( EC.element_to_be_clickable((By.XPATH,'//*[@id="botao-opcoes-lancamentos-2"]'))).click()
            buttonDownloadExcel = WebDriverWait(driver,10).until( EC.element_to_be_clickable((By.XPATH,'//*[@id="appController"]/div[3]/div/div[1]/div[1]/div/div[2]/div[3]/div/div/ul/li[2]/a'))).click()
        except Exception as e:
            logging.error(f'Failed to download invoice: {e}')
            raise e
        finally:
            logging.info('Download completedd successfully!')
    
    def _get_account_balance(self, driver:any) -> float:

        balanceAccordion = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="saldo-extrato-card-accordion"]/div[2]/voxel-icon/div/span'))).click()
        balance = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="saldo"]/ui-currency'))).text
        balance = float(balance.replace('R$ ','').replace(',','.'))

        return balance


    def get_banking_infos(self, download_path:str = f'{Path.home()}/Downloads' ) -> Union[float,str]:
        try:
            option = webdriver.ChromeOptions()
            option.add_argument('--no-sandbox')
            option.add_argument('disable-extensions')
            option.add_argument('start-maximized')
            option.add_experimental_option("prefs",{"download.default_directory":download_path})

            # driver = webdriver.Chrome(options=option)
            driver = webdriver.Remote(
                command_executor="http://chrome:4444",
                options=option
            )
            
            driver.get('https://www.itau.com.br/')

            self._login(driver)
            balance = self._get_account_balance(driver)
            downloadInvoice = self._download_credit_invoice(driver)

        except Exception as e:
            raise e
        else:
            return balance, f'{download_path}/Fatura-Excel.xls'
        finally:
            logging.info('Closing webpage!')
            time.sleep(3)
            driver.quit()

