import api_requests
import time
import requests
import json

from sql.sql import insert_wallet, select_wallet, update_wallet

if __name__ == '__main__':

    with open('email.json') as f:
        email = json.load(f)

    walletAddress = email["walletAddress"]

    # PEGA O NUMERO DE TRANSACOES DA CARTEIRA
    transaction_number = api_requests.get_api_response(walletAddress)
    # insere no banco
    id_of_new_row = insert_wallet(email["email"][0], walletAddress, transaction_number)

    old_transaction_number = select_wallet(walletAddress, id_of_new_row)
    #print("transaction_number", transaction_number)

    while True:
        #24horas
        waitOneDay = 60*60*24
        url = 'https://emailfastapi.herokuapp.com/email'
        contGetNewTransaction, amountOfTransactions = api_requests.get_new_status_transaction_number(old_transaction_number, walletAddress)
        old_transaction_number = select_wallet(walletAddress, id_of_new_row)
        print('contGetNewTransaction',contGetNewTransaction)
        print('amountOfTransactions',amountOfTransactions)

        #LIMITO O NUMERO DE TRANSACOES A 10
        if contGetNewTransaction < 10:
            if amountOfTransactions != old_transaction_number:
                print("Houve movimentacao na carteira.")
                sendEmail = requests.post(url, json=email)
                print(sendEmail.text)
                #UPDATE NO BD
                update_wallet(amountOfTransactions, id_of_new_row)
            else:
                print("Verificacao foi feita, mas nao houve movimentacao na carteira. ")
        else:
            break
        time.sleep(waitOneDay)
