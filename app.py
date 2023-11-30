from flask import Flask, render_template, request, jsonify

from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def home():
    return render_template('index.html')  # Replace 'your_html_file.html' with the actual name of your HTML file

@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.json.get('message', '')
    print(f"Received user input: {user_input}")
    bot_response = generate_bot_response(user_input)
    print(f"Bot response: {bot_response}")
    
    return jsonify({'response': bot_response})


def generate_bot_response(user_input):
    # Add your bot logic here
    # For simplicity, let's just echo the user input
    return f"You said: {user_input}"

if __name__ == '__main__':
    app.run(debug=True)
