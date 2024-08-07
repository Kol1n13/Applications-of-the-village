from flask import Flask, request, render_template, redirect, url_for
import database
import datetime

app = Flask(__name__)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        users = database.get_dictionary_of_users()
        if username in users and users[username][0] == password:
            return redirect(url_for(f'user_profile', isAuthenticated=True, id=users[username][1]))
        specialists = database.get_dictionary_of_specialists()
        if username in specialists and specialists[username][0] == password:
            return redirect(
                url_for('specialist_profile', id=specialists[username][1]))
        else:
            return render_template('login.html', error=True)
    else:
        return render_template('login.html', error=False)


@app.route('/user-profile', methods=['GET', 'POST'])
def user_profile():
    id = request.args.get('id')
    if request.method == 'POST' and request.form.get("dropdownValue") is not None:
        current_time = datetime.datetime.now().strftime("%H:%M:%S %d/%m/%Y")
        user_date = database.get_true_user_by_id(id)
        application_data = (
            database.count_applications() + 1, user_date[0][1], "Не задано",
            request.form["dropdownValue"], request.form["search"],
            current_time, "В ожидании", "Не задано", id, user_date[0][3],
            "Не задано", "None")
        database.add_application_to_db(application_data)
    elif request.method == 'POST' and request.form.get("delete") is not None:
        application_id = request.form.get("delete")
        database.delete_application(application_id)
    elif request.method == 'POST':
        new_phone_number = request.form["newPhoneNumber"]
        database.update_user_phone_number(id, new_phone_number)

    articles = database.get_user_by_id(user_id=id)
    if articles:
        articles.reverse()
    return render_template('user-profile.html', articles=articles)


##(1, "Turgeneva 4", "Александр", "Сантехника", "Трубы горят",
# '2004-08-30', 'Pending', 'саня', 1, "88003555311", "88003255711")


@app.route('/specialist-profile', methods=['GET', 'POST'])
def specialist_profile():
    id = request.args.get('id')
    if request.method == 'POST' and request.form.get("waitingTime") is not None:
        specialist_comment = request.form["waitingTime"]
        application_id = request.form["requestId"]
        database.update_application(application_id, id, specialist_comment)
    elif request.method == 'POST' and request.form.get("action") is not None:
        action = request.form.get("action")
        if action == "completed":
            application_id = request.form["requestId"]
            database.application_task_complete(application_id)
        else:
            application_id = request.form["requestId"]
            database.application_task_cancel(application_id)
    elif request.method == 'POST':
        new_phone_number = request.form["newPhoneNumber"]
        database.update_specialist_phone_number(id, new_phone_number)
    articles = database.search_applications_db1(id)
    return render_template('specialist-profile.html', articles=articles)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000)
