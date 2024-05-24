from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import flask
import json
import threading
import runner



app = Flask(__name__)
CORS(app)

@app.route("/")
def hello():
    return "Hello, World!"
@app.route('/users', methods=["GET", "POST"])
def users():
    print("users endpoint reached")
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
@app.route('/upload', methods=["POST"])
def upload():
    metadata = request.files['metadata'].read().decode('utf-8')
    json_data = json.loads(metadata)

    file = request.files['file']
    filename = secure_filename(file.filename).split('.')[0]
    antworten = lese_antworten_aus_datei(file)
    thread = threading.Thread(target=runner.runner(filename, json_data, antworten), args=(filename, json_data, antworten))
    thread.start()
    return jsonify({"status": "file uploaded"}), 200


def lese_antworten_aus_datei(file):
    # Dateiinhalt einlesen
    inhalt = file.read().decode('utf-8')

    # Antworten durch das Trennzeichen trennen
    antworten_roh = inhalt.split('###')

    # Jede Antwort und ihre Stichpunkte in eine Liste speichern
    antworten = [antwort.strip() for antwort in antworten_roh if antwort.strip()]
    return antworten


if __name__ == "__main__":
    app.run("localhost", 6969)
