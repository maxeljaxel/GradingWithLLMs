from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import flask
import json


app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"
@app.route('/users', methods=["GET", "POST"])
def users():
    print("users endpoint reached")
    if request.method == "GET":
        with open("users.json", "r") as f:
            data = json.load(f)
            data.append({
                "username":"user4",
                "pets": ["hamster"]
            })
            return flask.jsonify(data)
        
        
    if request.method == "POST":
        received_data = request.get_json()
        print(f"received data: {received_data}")
        message = received_data['data']
        return_data = {
            "status": "success",
            "message": f"received: {message}"
        }
        return flask.Response(response=json.dumps(return_data), status=201)
    
@app.route('/file', methods=["GET", "POST"])
def fileUpload():
    print("fileUpload reached")
    if request.method == "POST":
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(filename)
        print(filename)
        with open(filename, 'r') as f:
            first_line = f.readline()
            print('First line of the file:', first_line)

        return jsonify({"status": "file uploaded"}), 200
    else: 
        return jsonify({"status": "GET request received"}), 200

if __name__ == "__main__":
    app.run("localhost", 6969)