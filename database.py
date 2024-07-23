import sqlite3

db1_connect = sqlite3.connect('users.db')
db1_cursor = db1_connect.cursor()

users_list = [
    (1, 'Дружная 253', '1', '89533843071'),
    (2, 'Летняя 82', '2', '89222984020'),
]


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



db2_connect = sqlite3.connect('specialists.db')
db2_cursor = db2_connect.cursor()

specialists_list = [
    (1, 'Александр', '1', '89024109226'),
    (2, 'Сергей', '2', '89826761524')
]


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


#specialists_db(specialists_list)

db3_connect = sqlite3.connect('application.db')
db3_cursor = db3_connect.cursor()

application_list = [
    (1, "Turgeneva 4", "Александр", "Электричество", "При включении ", '2024-01-08',
     'В ожидании', 'Не задано', 1, "89533843071", "Не задано", "None"),
]


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
        specialist_phone TEXT,
        specialist_comment
    )
    """)
    db3_cursor.executemany(
        "INSERT INTO application VALUES(?,?,?,?,?,?,?,?,?,?,?,?);",
        data_of_application)
    db3_connect.commit()


#application_db(application_list)


def search_users_db():
    with sqlite3.connect('users.db') as connection:
        cursor = connection.cursor()
        cursor.execute(f"SELECT * FROM users")
        all_results = cursor.fetchall()
    return all_results


def search_applications_db(id):
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

def search_applications_db1(specialist_id):
    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM application WHERE specialist_name = ? "
                       "OR application_status = 'В ожидании'", (find_login_by_id(specialist_id),))
        all_results = cursor.fetchall()
    return all_results


def get_dictionary_of_specialists():
    data = search_specialists_db()
    result = {}
    for specialist in data:
        result[specialist[1]] = (specialist[2], specialist[0])
    return result


def is_user_registered(id):
    data = search_users_db()
    for user in data:
        if user[1] == id:
            return True
    return False


def is_spec_registered(id):
    data = search_specialists_db()
    for spec in data:
        if spec[1] == id:
            return True
    return False


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
        query = f"INSERT INTO application VALUES ({placeholders})"
        cursor.execute(query, values)
        connection.commit()



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


def update_specialist_phone_number(specialist_id, new_phone_number):
    with sqlite3.connect('specialists.db') as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE specialists SET specialists_phone_number = ? WHERE specialists_id = ?",
                       (new_phone_number, specialist_id))
        connection.commit()

    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()
        cursor.execute("UPDATE application SET specialist_phone = ? WHERE specialist_name = ?",
                       (new_phone_number, find_login_by_id(specialist_id)))
        connection.commit()


# user_data_by_id = get_user_by_id(db1_cursor, 1)
# print(user_data_by_id)

def find_login_by_id(specialist_id):
    with sqlite3.connect('specialists.db') as connection:
        cursor = connection.cursor()
        sql_query = "SELECT specialists_login FROM specialists WHERE specialists_id = ?"

        cursor.execute(sql_query, (specialist_id,))

        result = cursor.fetchone()

        if result:
            return result[0]  # Возвращаем первый столбец (логин)
        else:
            return None  # Если id не найден, возвращаем None


def update_application(application_id, specialist_id, specialist_comment):
    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()

        # Update specialist information in the application table
        cursor.execute("""
            UPDATE application 
            SET specialist_name = ?,
                specialist_phone = ?,
                application_status = ? 
            WHERE application_id = ?
        """, (
            find_login_by_id(specialist_id), get_specialist_phone_by_id(specialist_id), 'Выполняется', application_id))

        # Insert specialist comment into the application table
        cursor.execute("""
            UPDATE application 
            SET specialist_comment = ? 
            WHERE application_id = ?
        """, (specialist_comment, application_id))

        connection.commit()


def get_specialist_phone_by_id(specialist_id):
    with sqlite3.connect('specialists.db') as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT specialists_phone_number FROM specialists WHERE specialists_id = ?", (specialist_id,))
        phone_number = cursor.fetchone()[0]
    return phone_number


# Example usage:
# update_application(application_id=1, specialist_id=1, specialist_comment="Fixed the issue.")

def application_task_complete(application_id):
    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()

        # Update application status to "completed"
        cursor.execute("""
            UPDATE application 
            SET application_status = 'Выполнено' 
            WHERE application_id = ?
        """, (application_id,))

        connection.commit()


# Example usage:
# application_task_complete(application_id=1)

def application_task_cancel(application_id):
    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()

        # Update application fields for the specified application_id
        cursor.execute("""
            UPDATE application 
            SET specialist_name = 'не назначен специалист',
                specialist_phone = 'не назначен специалист',
                application_status = 'В ожидании',
                specialist_comment = 'не назначен специалист' 
            WHERE application_id = ?
        """, (application_id,))

        connection.commit()

# Example usage:
# application_task_cancel(application_id=1)

def delete_application(application_id):
    with sqlite3.connect('application.db') as connection:
        cursor = connection.cursor()

        # Delete the application with the specified application_id
        cursor.execute("DELETE FROM application WHERE application_id = ?", (application_id,))

        connection.commit()

# Example usage:
# delete_application(application_id=1)