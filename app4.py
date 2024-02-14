from res import generate_response


import torch

import time
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from torch import cuda, bfloat16, cuda, float32
app = Flask(__name__)
CORS(app)





@app.route('/')
def home():
    return render_template('index3.html')  # Replace 'your_html_file.html' with the actual name of your HTML file

@app.route('/get_response', methods=['POST'])
def get_response():
    question = request.json.get("message","")
    # print("question: ",question)
    start_time = time.time()
    bot_response = generate_response(question)

    end_time = time.time()
    total_time = end_time - start_time
    total_time = round(total_time,2)
    print("Answer: ",bot_response.strip().replace("\n\n","\n"))
    print(f"*******Total Time taken to answer: ",total_time)
    torch.cuda.empty_cache()
    return jsonify({'response': bot_response.strip().replace("\n\n","\n").replace("\n","</br>"),'reponse_time':str(total_time)})


if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True,use_reloader= False)
