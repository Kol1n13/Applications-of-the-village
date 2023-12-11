from flask import Flask, request, render_template
import database

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = database.get_dictionary_of_users()
        if username in users:
            if users[username] == password:
                return 'Вы вошли в систему!'
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')


if __name__ == '__main__':
    app.run()
