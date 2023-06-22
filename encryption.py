import json
import os
import hashlib

from twilio.rest import Client
from flask import Flask, render_template, request, session, make_response, flash, url_for, redirect, jsonify

app = Flask(__name__)

@app.route('/data', methods=['GET'])
def get_data():
    data = {
        'name': 'John Doe',
        'age': 30,
        'city': 'New York'
    }
    return jsonify(data)

@app.route("/", methods=["GET", "POST"])
def index():
    with open("chat0001.json", "r") as f:
        data = json.load(f)
    json_data = json.dumps(data)
    print(json_data)
    return render_template('myai.html', json_data=json_data)

if __name__ == '__main__':
    app.run(debug=True)
