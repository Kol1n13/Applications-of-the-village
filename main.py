import sqlite3

db1_connect = sqlite3.connect('users.db')
db1_cursor = db1_connect.cursor()

users_list = [
    (1, 'Turgeneva 4', 'Durka'),
    (2, 'Lenina 51', 'x2 Durka'),
    (3, 'Kraulya 73', 'OldHome')
]  # get data of users


def users_db(data_of_users):
    db1_cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        user_login TEXT,
        user_password TEXT
    )
    """)
    db1_cursor.executemany("INSERT INTO users (user_login, user_password) VALUES (?, ?);",
                           [(user[1], user[2]) for user in data_of_users])
    db1_connect.commit()


users_db(users_list)

db2_connect = sqlite3.connect('specialists.db')
db2_cursor = db2_connect.cursor()

specialists_list = [
    (1, 'Дрочислав Сын Сергея', 'Vodka'),
    (2, 'Артём', 'Pivo')
]  # get data of specialists


def specialists_db(data_of_specialists):
    db2_cursor.execute("""CREATE TABLE IF NOT EXISTS specialists(
        specialists_id INTEGER PRIMARY KEY,
        specialists_login TEXT,
        specialists_password TEXT
    )
    """)
    db2_cursor.executemany("INSERT INTO specialists VALUES(?,?,?);", data_of_specialists)  # filled in the database
    db2_connect.commit()


specialists_db(specialists_list)

db3_connect = sqlite3.connect('application.db')
db3_cursor = db3_connect.cursor()

application_list = [
    (1, '2004-08-30', 'Turgeneva 4', 'Pending', 'John Doe')
]  # get application of application


def application_db(data_of_application):
    db3_cursor.execute("""CREATE TABLE IF NOT EXISTS application(
        application_id INTEGER PRIMARY KEY,
        application_date DATE,
        application_address TEXT,
        application_status TEXT,
        specialists TEXT
    )
    """)
    db3_cursor.executemany("INSERT INTO application VALUES(?,?,?,?,?);", data_of_application)
    db3_connect.commit()



application_db(application_list)


def search_db(cursor, table_name):  # return all data from DB in list
    cursor.execute(f"SELECT * FROM {table_name}")
    all_results = cursor.fetchall()
    return all_results


def add_to_table(cursor, connection, table_name, values):  # add value to table_name
    placeholders = ', '.join(['?' for _ in values])
    query = f"INSERT INTO {table_name} VALUES ({placeholders});"
    cursor.execute(query, values)
    connection.commit()
