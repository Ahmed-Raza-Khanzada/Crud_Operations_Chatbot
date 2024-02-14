import json
import logging
import time
from threading import Thread

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import requests



app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@app.route('/')
def home():
    return render_template('index.html')


def give_response(question,uuid):
    try:
        r = requests.post('http://localhost:5050/api/generate',
                          json={
                              'model': "Liqchatllama2",#Liqchat3,Liqchatmistral
                              'prompt': question,
                              "num_thread":100
                          },
                          stream=True)

        r.raise_for_status()

        for line in r.iter_lines():
            body = json.loads(line)
            response_part = body.get('response', '')
            print(response_part, end=" ", flush=True)
            socketio.emit('response_part', {'response_part': response_part,"uuid":uuid})

            if 'error' in body:
                raise Exception(body['error'])

            if body.get('done', False):
                break
    except Exception as e:
        logging.error(f"Error in generate function: {str(e)}")
        print(e)
        return ""

@app.route('/get_response', methods=['POST'])
def get_response():
    question = request.json.get("message", "")
    uuid = request.json.get("uuid","")  
    print("question: ", question)
    start_time = time.time()
    # Use threading for concurrent requests
    thread = Thread(target=give_response, args=(question,uuid))
    thread.start()
    thread.join()

    end_time = time.time()
    total_time = round(end_time - start_time, 2)
  
    print(f"Total Time taken to answer: {total_time} seconds")

    return jsonify({'response': "True",
                    'response_time': str(total_time)})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)