import sqlite3

db1_connect = sqlite3.connect('users.db')
db1_cursor = db1_connect.cursor()

users_list = [
    (1, 'Turgeneva 4', 'Durka', '88003555311'),
    (2, 'Lenina 51', 'x2 Durka', '88003555511'),
    (3, 'Kraulya 73', 'OldHome', '88003555711')
]  # get data of users


def users_db(data_of_users):
    db1_cursor.execute("""CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY,
        user_login TEXT,
        user_password TEXT,
        user_phone_number TEXT
    )
    """)
    db1_cursor.executemany("INSERT INTO users VALUES(?,?,?,?);", users_list)
    db1_connect.commit()


# users_db(users_list)

db2_connect = sqlite3.connect('specialists.db')
db2_cursor = db2_connect.cursor()

specialists_list = [
    (1, 'Дрочислав Сын Сергея', 'Vodka', '88003255711'),
    (2, 'Артём', 'Pivo', '88001553711')
]  # get data of specialists


def specialists_db(data_of_specialists):
    db2_cursor.execute("""CREATE TABLE IF NOT EXISTS specialists(
        specialists_id INTEGER PRIMARY KEY,
        specialists_login TEXT,
        specialists_password TEXT,
        specialists_phone_number INTEGER
    )
    """)
    db2_cursor.executemany("INSERT INTO specialists VALUES(?,?,?,?);",
                           data_of_specialists)  # filled in the database
    db2_connect.commit()


# specialists_db(specialists_list)

db3_connect = sqlite3.connect('application.db')
db3_cursor = db3_connect.cursor()

application_list = [
    (1, 3, '2004-08-30', 'Pending', 'John Doe', 'туалет засрался'),
    (2, 2, '2002-02-22', 'Pending', 'John Snow', "трубу прорвало")
]  # get application of application


def application_db(data_of_application):
    db3_cursor.execute("""CREATE TABLE IF NOT EXISTS application(
        application_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        application_date DATE,
        application_status TEXT,
        specialists TEXT,
        comment TEXT
    )
    """)
    db3_cursor.executemany("INSERT INTO application VALUES(?,?,?,?,?,?);", data_of_application)
    db3_connect.commit()



#application_db(application_list)


def search_users_db():
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users")
        all_results = cursor.fetchall()
    return all_results


def search_specialists_db():
    with sqlite3.connect('specialists.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM specialists")
        all_results = cursor.fetchall()
    return all_results

def search_application_db():
    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM application")
        all_results = cursor.fetchall()
    return all_results

#print(search_application_db())

def get_dictionary_of_specialists():
    data = search_specialists_db()
    result = {}
    for specialist in data:
        result[specialist[1]] = specialist[2]
    return result




def get_dictionary_of_users():
    data = search_users_db()
    result = {}
    for user in data:
        result[user[1]] = user[2]
    return result




def add_to_table(cursor, connection, table_name,
                 values):  # add value to table_name
    placeholders = ', '.join(['?' for _ in values])
    query = f"INSERT INTO {table_name} VALUES ({placeholders});"
    cursor.execute(query, values)
    connection.commit()


# print(get_dictionary_of_users())


def get_user_by_id(cursor, user_id):
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user_data = cursor.fetchone()
    if user_data:
        _, user_login, _, user_phone_number = user_data
        return user_login, user_phone_number
    else:
        return "Пользователь не найден."

# user_data_by_id = get_user_by_id(db1_cursor, 1)
# print(user_data_by_id)

def get_data_to_httml():
    data_app = search_application_db()
    result = []
    for application in data_app:
        id_of_user = application[1]
        data_of_user = get_user_by_id(db1_cursor, id_of_user)
        tuple_of_data = (application[0], data_of_user[0], application[5], data_of_user[1])
        result.append(tuple_of_data)
    return result


print(get_data_to_httml())

