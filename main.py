from flask import Flask, request, jsonify

app = Flask(__name__)

# Dummy database to store user settings
users = {}

@app.route('/activate_secure_private_mode', methods=['POST'])
def activate_secure_private_mode():
    user_id = request.json.get('user_id')
    duration = request.json.get('duration')
    contacts = request.json.get('contacts')

    # Store user settings in the database
    users[user_id] = {
        'secure_private_mode': True,
        'duration': duration,
        'contacts': contacts
    }

    return jsonify({'message': 'Secure Private Mode activated successfully'})

@app.route('/deactivate_secure_private_mode', methods=['POST'])
def deactivate_secure_private_mode():
    user_id = request.json.get('user_id')

    # Remove user settings from the database
    users.pop(user_id, None)

    return jsonify({'message': 'Secure Private Mode deactivated successfully'})

if __name__ == '__main__':
    app.run(debug=True)
