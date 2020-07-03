from datetime import date
from flask import Flask, jsonify, request
app = Flask(__name__)

users = {
    "username": {"password": "pswd", "moods": []}
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


if __name__ == '__main__':
    app.run(debug=True)
