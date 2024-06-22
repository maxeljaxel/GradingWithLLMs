import json
import os
import threading
from datetime import datetime
from multiprocessing import Manager
from wsgiref.types import InputStream

from flask import Flask, jsonify, request, send_file, Response
from flask_cors import CORS
from werkzeug.utils import secure_filename

import gpt_querier

app = Flask(__name__)
CORS(app, expose_headers=['Content-Disposition'])


@app.route('/upload', methods=["POST"])
def upload():
    task_id = datetime.now().strftime('%Y%m%d%H%M%S%f')
    metadata = request.files['metadata'].read().decode('utf-8')
    json_data = json.loads(metadata)

    file = request.files['file']
    filename = secure_filename(file.filename).split('.')[0]
    answers = convert_file_content_into_list(file)
    tasks[task_id] = {"status": "processing", "progress": f" 0 of {len(answers)}"}
    thread = threading.Thread(target=gpt_querier.query_run,
                              args=(task_id, filename, json_data, answers, tasks))
    thread.start()
    return jsonify({"status": "file uploaded", "taskId": task_id}), 200


@app.route('/download/<taskId>', methods=["GET"])
def getFile(taskId):
    task = tasks[taskId]
    status = task["status"]
    if status == "processing":
        progress = task["progress"]
        return jsonify({"status": "processing", "progress": f"{progress}"}), 200
    if status == "Done":
        file_name = task["fileName"]
        try:
            with open(file_name, 'r') as datei:
                # safe content into a temporary file
                datei_inhalt = datei.read()
            # delete the file from the server
            os.remove(file_name)
            response = Response(datei_inhalt, mimetype='application/octet-stream')
            response.headers.set('Content-Disposition', 'attachment', filename=os.path.basename(file_name))

            # create a Response object and return it with Response 200
            return response, 200
        except FileNotFoundError:
            return "Datei nicht gefunden", 404


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
    manager = Manager()
    tasks = manager.dict()
    app.run("localhost", 6969)
