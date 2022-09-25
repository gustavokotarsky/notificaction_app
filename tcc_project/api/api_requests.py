import email
import requests
from tornado.web import url


def get_api_response(walletAddress):
    try:
        response = requests.get(f"https://blockchain.info/balance?active={walletAddress}")
        transaction_number = response.json()[walletAddress]['n_tx']
        return transaction_number
    except Exception as e:
        print('Oops!', e.__class__, 'occurred.')


def get_new_status_transaction_number(old_transaction_number, walletAddress):
    new_transaction_number = get_api_response(walletAddress)
    cont = 0
    if (new_transaction_number != old_transaction_number) & (cont < 10):
        #old_transaction_number = new_transaction_number
        cont + 1
        print(f'Old transaction number was: {old_transaction_number} and now is: {new_transaction_number}')
    return cont, new_transaction_number
