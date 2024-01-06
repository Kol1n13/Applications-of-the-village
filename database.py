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
    (1, 'саня', 'водка', '88003255711'),
    (2, 'артем', 'пиво', '88001553711')
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
    (1, "Turgeneva 4", "Александр", "Сантехника", "Трубы горят", '2004-08-30',
     'Pending', 'саня', 1, "88003555311", "88003255711"),
    (2, "Lenina 51", "Никита", "Сетевое оборудование", "Роутер сломался",
     '2002-02-22', 'Pending', 'саня', 2, "88003555511", "88003255711"),
    (3, "Turgeneva 4", "Александр", "Проблема со здоровьем", "Висячий",
     "2050-02-11", 'Pending', 'саня', 1, "88003555311", "88003255711")
]  # get application of application


def application_db(data_of_application):
    db3_cursor.execute("""CREATE TABLE IF NOT EXISTS application(
        application_id INTEGER PRIMARY KEY,
        user_login TEXT,
        user_name TEXT,
        theme TEXT,
        user_comment TEXT,
        application_date DATE,
        application_status TEXT,
        specialist_name TEXT,
        user_id INTEGER,
        user_phone TEXT,
        specialist_phone TEXT
    )
    """)
    db3_cursor.executemany(
        "INSERT INTO application VALUES(?,?,?,?,?,?,?,?,?,?,?);",
        data_of_application)
    db3_connect.commit()


# application_db(application_list)


def search_users_db():
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users")
        all_results = cursor.fetchall()
    return all_results


def search_applications_db():
    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM application")
        all_results = cursor.fetchall()
    return all_results


def search_specialists_db():
    with sqlite3.connect('specialists.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM specialists")
        all_results = cursor.fetchall()
    return all_results


def get_dictionary_of_specialists():
    data = search_specialists_db()
    result = {}
    for specialist in data:
        result[specialist[1]] = (specialist[2], specialist[0])
    return result


def get_dictionary_of_users():
    data = search_users_db()
    result = {}
    for user in data:
        result[user[1]] = (user[2], user[0])
    return result


def add_to_table(cursor, connection, table_name,
                 values):  # add value to table_name
    placeholders = ', '.join(['?' for _ in values])
    query = f"INSERT INTO {table_name} VALUES ({placeholders});"
    cursor.execute(query, values)
    connection.commit()

def count_applications():
    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM application")
        count = cursor.fetchone()[0]
    return count



# print(get_dictionary_of_users())


def get_user_by_id(user_id):
    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM application WHERE user_id = ?",
                       (user_id,))
        user_data = cursor.fetchall()
        if user_data:
            return user_data
        else:
            return None

def add_application_to_db(values):
    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()
        placeholders = ', '.join(['?' for _ in values])
        query = f"INSERT INTO application VALUES ({placeholders});"
        cursor.execute(query, values)

def get_true_user_by_id(user_id):
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        user_data = cursor.fetchall()
        if user_data:
            return user_data
        else:
            return None


def update_user_phone_number(user_id, new_phone_number):
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE users SET user_phone_number = ? WHERE user_id = ?", (new_phone_number, user_id))
        connection.commit()

    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE application SET user_phone = ? WHERE user_id = ?", (new_phone_number, user_id))
        connection.commit()


# user_data_by_id = get_user_by_id(db1_cursor, 1)
# print(user_data_by_id)
