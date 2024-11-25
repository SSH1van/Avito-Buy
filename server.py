from flask import Flask, request, jsonify
from waitress import serve
from dotenv import load_dotenv
import base64
import re
import os


app = Flask(__name__)

USERNAME = os.getenv('USERNAME')
PASSWORD = os.getenv('PASSWORD')
FILE_PATH = "code.txt"

def check_auth(auth_header):
    if not auth_header:
        return False
    try:
        auth_type, credentials = auth_header.split(" ", 1)
        if auth_type.lower() != "basic":
            return False
        decoded_credentials = base64.b64decode(credentials).decode("utf-8")
        username, password = decoded_credentials.split(":", 1)
        return username == USERNAME and password == PASSWORD
    except Exception:
        return False

def get_part_message(data):
    pattern = r"(?<!\S)\d{4}(?!\S)"
    match = re.search(pattern, data)
    if not match:
        return jsonify({"error": "Invalid input"}), 401
    return match.group()

@app.route("/", methods=["POST"])
def receive_sms():
    auth_header = request.headers.get("Authorization")
    if not check_auth(auth_header):
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_data(as_text=True)
    code = get_part_message(data)

    with open(FILE_PATH, "w") as f:
        f.write(code)

    return {"status": "success"}

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=8080)