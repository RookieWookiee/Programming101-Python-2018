import hashlib
import psycopg2
from client import Client

conn = psycopg2.connect("dbname=bank user=<some_username>")
cursor = conn.cursor()


def create_clients_table():
    create_query = '''create table if not exists
        clients(id SERIAL PRIMARY KEY,
                username VARCHAR(128),
                password VARCHAR(128),
                balance REAL DEFAULT 0,
                message TEXT)'''

    cursor.execute(create_query)


def change_message(new_message, logged_user):
    update_sql = "UPDATE clients SET message = '%s' WHERE id = '%s'" % (new_message, logged_user.get_id())
    cursor.execute(update_sql)
    conn.commit()
    logged_user.set_message(new_message)


def change_pass(new_pass, logged_user):
    update_sql = "UPDATE clients SET password = '%s' WHERE id = '%s'" % (new_pass, logged_user.get_id())
    cursor.execute(update_sql)
    conn.commit()


def register(username, password):
    hash = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        username.encode(),
        10000
    ).hex()
    insert_sql = "INSERT INTO clients (username, password) VALUES (%s, %s)"
    cursor.execute(insert_sql, (username, str(hash)))
    conn.commit()


def login(username, password):
    select_query = "SELECT id, username, balance, message FROM clients"
    cursor.execute(select_query)
    select_query = "SELECT id, username, balance, message FROM clients WHERE username = '%s' AND password = '%s' LIMIT 1" % (username, password)

    cursor.execute(select_query)
    user = cursor.fetchone()

    if(user):
        return Client(user[0], user[1], user[2], user[3])
    else:
        return False
