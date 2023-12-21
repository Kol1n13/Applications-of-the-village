from flask import Flask, request, render_template, redirect, url_for
import database

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = database.get_dictionary_of_users()
        if username in users and users[username] == password:
            return redirect(url_for('user_profile'))
        specialists = database.get_dictionary_of_specialists()
        if username in specialists and specialists[username] == password:
            return redirect(url_for('specialist_profile'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/user-profile')
def user_profile():
    return 'Пользователь зашел в систему!'


@app.route('/specialist-profile')
def specialist_profile():
    return 'Специалист зашел в систему!'


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
