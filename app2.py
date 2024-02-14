import torch
import transformers
from transformers import pipeline
import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
import requests
import ast
import logging
from torch import cuda, bfloat16, cuda, float32

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index2.html')  

def give_reponse(question):
    
    try:
        r = requests.post('http://localhost:11434/api/generate',
                            json={
                                'model': "Liqchat3",
                                'prompt': question
                            },
                            stream=True)
        r.raise_for_status()
        
        response_parts = []  # To store individual parts of the response

        for line in r.iter_lines():
            
            body = json.loads(line)
            # print(body)
            response_part = body.get('response', '')

    #         print(response_part, end='', flush=True)
    #         response_parts.append(response_part)

    #         if 'error' in body:
    #             raise Exception(body['error'])

    #         if body.get('done', False):
    #             return " ".join(response_parts)
    except Exception as e:
        logging.error(f"Error in generate function: {str(e)}")
        print(e)
        return ""


@app.route('/get_response', methods=['POST'])
def get_response():
    question = request.json.get("message","")
    print("question: ",question)
    start_time = time.time()
    bot_response = give_reponse(question)
    end_time = time.time()
    total_time = end_time - start_time
    total_time = round(total_time,2)
    print("Answer: ",bot_response.strip().replace("\n\n","\n"))
    print(f"*******Total Time taken to answer: ",total_time)
    torch.cuda.empty_cache()
    socketio.emit('response_part', {'response_part': response_part})
    return jsonify({'response': bot_response.strip().replace("\n\n","\n").replace("\n","</br>"),'reponse_time':str(total_time)})


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)
