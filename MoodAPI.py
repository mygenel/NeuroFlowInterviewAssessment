from datetime import date
from flask import Flask, jsonify, request
app = Flask(__name__)

users = {
    "username": {"password": "pswd", "moods": [], 'loggedIn': False}
}


@app.route('/mood', methods=['GET', 'POST'])
def mood():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        mood = data['mood']
        if username in users:
            users[username]['moods'].append(
                {'mood': mood, 'date': date.today()})
            return jsonify({'mood': users[data['username']]['moods']}), 201
        else:
            return jsonify({'message': "There is no such user"}), 404


@app.route('/login', methods=['POST'])
def login():
    loginData = request.get_json()
    username = loginData['username']
    password = loginData['password']
    if username in users and users[username]['password'] == password:
        users[username]['loggedIn'] = True
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'message': "Wrong username or password"}), 403


if __name__ == '__main__':
    app.run(debug=True)
