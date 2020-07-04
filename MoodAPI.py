from datetime import date
from flask import Flask, jsonify, request
app = Flask(__name__)


users = {
    "username": {"password": "pswd", "moods": [], 'loggedIn': False}
}


def getStreak(moods):
    if len(moods) <= 1:
        return len(moods)
    i = len(moods) - 2
    streak = 1
    while i >= 0 and (moods[i+1]['date'] - moods[i]['date']).days <= 1:
        print((moods[i+1]['date'] - moods[i]['date']).days)
        if (moods[i+1]['date'] - moods[i]['date']).days == 1:
            streak += 1
        i -= 1
    return streak


@app.route('/mood', methods=['GET', 'POST'])
def mood():
    data = request.get_json()
    username = data['username']
    if username in users:
        if not users[username]['loggedIn']:
            return jsonify({'message': 'User is not logged in'}), 403

        if request.method == 'POST':
            mood = data['mood']
            users[username]['moods'].append(
                {'mood': mood, 'date': date.today()})
            return jsonify({'mood': users[data['username']]['moods'], 'streak': getStreak(users[data['username']]['moods'])}), 201
        else:
            return jsonify({'mood': users[data['username']]['moods'], 'streak': getStreak(users[data['username']]['moods'])}), 201
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
    app.run()
