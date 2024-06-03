from flask import Flask, jsonify, request
from flask_cors import CORS
from werkzeug.utils import secure_filename
import flask
import json
import threading
import gpt_querier

app = Flask(__name__)
CORS(app)


#TODO: Delete? 
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
    answers = convert_file_content_into_list(file)
    thread = threading.Thread(target=gpt_querier.query_run,
                              args=(filename, json_data, answers,))
    thread.start()
    return jsonify({"status": "file uploaded"}), 200


def convert_file_content_into_list(file):
    """
    Method to convert the file content into a list. It uses as default the separator symbol '###' and only works with
    this separator
    :param file: the file to be converted containing the answers
    :return: list of answers
    """
    # read file content
    inhalt = file.read().decode('utf-8')

    # split answers with the separater symbol
    antworten_roh = inhalt.split('###')

    # safe every answer in list
    antworten = [antwort.strip() for antwort in antworten_roh if antwort.strip()]
    return antworten


if __name__ == "__main__":
    app.run("localhost", 6969)
