from configparser import ConfigParser
from pyitau import Itau
from whatsapp import Whatsapp
import pandas as pd, logging

logging.basicConfig(level=logging.INFO,format='%(asctime)s - %(levelname)s -> %(message)s')
logging.getLogger()

def divide_balance(phone_number:str, agency:str, account:str, account_digit:str, password:str):

     logging.info('Starting divide balance function...')
     try:
          logging.info('Connecting to bank account')
          itau_client = Itau(agency=agency, account=account, account_digit=account_digit, password=password)
          itau_client.authenticate()
          logging.info('Connection complete.')

          account_balance = itau_client.get_statements()['saldoResumido']
          balance = float(account_balance["saldoContaCorrente"]['valor'].replace('.', '').replace(',', '.'))

          if balance > 0:
               logging.info('Calculating division of the account balance...')
               
               fifty_percent = (0.5 * balance)
               thirty_percent = (0.3 * balance)
               twenty_percent = (0.2 * balance)
               
               logging.info('Division has been completed!')

               logging.info('Send whatsapp menssage...')

               message = f'O saldo na conta esta no valor de: *R${balance:,.2f}*\n\nSegue abaixo as divisões que eu fiz para que você possa gastar esse valor de forma inteligente:\n\nValor para despesas fixas: *R${fifty_percent:,.2f}*\nValor para gastos pessoais: *R${thirty_percent:,.2f}*\nValor para investir: *R${twenty_percent:,.2f}* \n\n\n*Obs:* Em breve trarei o extrato do cartão!!!'

               whats_client = Whatsapp()
               whats_client.send_message(phone_number,message)

          else:
               logging.warning('Account balance is empty!')

     except Exception as e:
          raise e

     finally:
          logging.info('Complete divide balance function!')

if __name__=="__main__":

     config = ConfigParser()
     config.read('credentials.ini')

     agency = config['ITAU']['agencia']
     account = config['ITAU']['conta']
     account_digit = config['ITAU']['digito']
     password = config['ITAU']['senha']
     phone = '+5511969537543'

     divide_balance(phone,agency,account, account_digit, password)