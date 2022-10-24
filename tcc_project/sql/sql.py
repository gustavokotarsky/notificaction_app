import psycopg2
from core import settings


def db_connection():
    return psycopg2.connect(
        database=settings.DATABASE,
        user=settings.USER,
        password=settings.PASSWORD,
        host=settings.HOST,
        port=settings.PORT
    )


def select_wallet(walletAddress, id_of_new_row):
    try:
        # read connection parameters
        conn = db_connection()

        conn.autocommit = True

        cursor = conn.cursor()

        cursor.execute("""SELECT transaction_number from wallet_monitor where id= %s""", (id_of_new_row,))

        transaction_number = cursor.fetchone()
        # print("transaction_number from sql", transaction_number[0])

        conn.commit()
        conn.close()

        return transaction_number[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')


def insert_wallet(email, walletAddress, transaction_number):
    # params = db_config()

    conn = db_connection()

    # conn = psycopg2.connect(**params)

    conn.autocommit = True

    cursor = conn.cursor()

    sql = """INSERT INTO wallet_monitor (ID,email,wallet_address,transaction_number) VALUES (DEFAULT, %s, %s, %s)"""
    cursor.execute(sql, (email, walletAddress, transaction_number))
    # PEGA ID DO INSERT FEITO
    cursor.execute('SELECT LASTVAL()')
    id_of_new_row = cursor.fetchone()[0]

    conn.commit()
    # print("Records inserted.")
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

        # print("transaction_number from sql", transaction_number[0])

        conn.commit()
        conn.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            # print('Database connection closed.')
