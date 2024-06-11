from flask import Flask, jsonify
import os

app = Flask(__name__)

# Get the server ID from the environment variable
server_id = os.environ.get('SERVER_ID', 'Unknown')


@app.route('/home', methods=['GET'])
def home():
    message = f"Hello from Server: {server_id}"
    return jsonify({"message": message, "status": "successful"}), 200


@app.route('/heartbeat', methods=['GET'])
def heartbeat():
    return '', 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
