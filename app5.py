import json
import logging
import time
from threading import Thread

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import requests

from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama



app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

@app.route('/')
def home():
    r2 = request.args.get("currentpage")
    print(r2,"????????????????????????????????????????????????????")
    return render_template('index.html')
llm = Ollama(
    model="Liqchatbotv12", 
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
)

def give_response(question,uuid):
    try:
        a=""

        for line in llm.stream(question):
          
            socketio.emit('response_part', {'response_part': line,"uuid":uuid})
            a+= line
        return a
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
    # # Use threading for concurrent requests
    # thread = Thread(target=give_response, args=(question,uuid))
    # thread.start()
    # thread.join()

    ret1 = give_response(question,uuid)
    end_time = time.time()
    total_time = round(end_time - start_time, 2)
  
    print(f"Total Time taken to answer: {total_time} seconds")

    return jsonify({'response': ret1,
                    'response_time': str(total_time)})

if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)
