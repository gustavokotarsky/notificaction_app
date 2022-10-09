import configparser

import psycopg2
from configparser import ConfigParser

from distlib import database

import config

def db_connection():
    return psycopg2.connect(
        database="df8hlqn7scsg4p",
        user='fbmybewpitzeje',
        password='ef0a6ad988164f364f384c9f1cc89101a53bbca87a1df94b464e5ba2c1cb722a',
        host='ec2-44-210-50-83.compute-1.amazonaws.com',
        port='5432'
    )

def select_wallet(walletAddress, id_of_new_row):
    try:
        # read connection parameters
        conn = db_connection()

        conn.autocommit = True

        cursor = conn.cursor()

        cursor.execute("""SELECT transaction_number from wallet_monitor where id= %s""", (id_of_new_row,))

        transaction_number = cursor.fetchone()
        #print("transaction_number from sql", transaction_number[0])

        conn.commit()
        conn.close()

        return transaction_number[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')


def insert_wallet(email, walletAddress, transaction_number):
    #params = db_config()

    conn = db_connection()

    #conn = psycopg2.connect(**params)

    conn.autocommit = True

    cursor = conn.cursor()



    sql = """INSERT INTO wallet_monitor (ID,email,wallet_address,transaction_number) VALUES (DEFAULT, %s, %s, %s)"""
    cursor.execute(sql, (email, walletAddress, transaction_number))
    #PEGA ID DO INSERT FEITO
    cursor.execute('SELECT LASTVAL()')
    id_of_new_row = cursor.fetchone()[0]

    conn.commit()
    #print("Records inserted.")
    conn.close()
    return id_of_new_row


def update_wallet(new_amout_of_transactions, id_of_new_row):
    try:
        # read connection parameters
        conn = db_connection()

        conn.autocommit = True

        cursor = conn.cursor()

        cursor.execute("""UPDATE wallet_monitor set transaction_number = %s where id= %s""",
                       (new_amout_of_transactions, id_of_new_row,))

        #print("transaction_number from sql", transaction_number[0])

        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            #print('Database connection closed.')

#if __name__ == '__main__':
    #select_wallet()
    #insert_wallet('gukotarsky@gmail.com', '329koRvovTyNnd4ADrpR2uJHzXxfvKxta5', '1001')
