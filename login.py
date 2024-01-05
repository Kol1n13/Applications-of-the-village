from flask import Flask, request, render_template, redirect, url_for
import database

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = database.get_dictionary_of_users()
        if username in users and users[username][0] == password:
            return redirect(url_for(f'user_profile', id=users[username][1]))
        specialists = database.get_dictionary_of_specialists()
        if username in specialists and specialists[username][0] == password:
            return redirect(url_for('specialist_profile', id=specialists[username][1]))
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=False)


@app.route('/user-profile/<int:id>', methods=['GET', 'POST'])
def user_profile(id):
    if request.method == 'POST':
        print(request.form["search"])
    articles = database.get_user_by_id(user_id=id)
    return render_template('user-profile.html', articles=articles)


@app.route('/specialist-profile')
def specialist_profile():
    articles = database.search_applications_db()
    return render_template('specialist-profile.html', articles=articles)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
