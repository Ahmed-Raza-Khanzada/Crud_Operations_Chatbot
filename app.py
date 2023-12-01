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

def create_user(): return 


def generate_bot_response(user_input):
    # Add your bot logic here
    # For simplicity, let's just echo the user input
    default_action = None
    categories_names,categories = get_availaible_categories()
    print("Type 'exit' to end the conversation.")

    instruct = f"""Statudos is a website providing information about influencers and their status based on personal categories ({categories_names}). You are a Statudos WhatsApp bot with the role of offering details about Statudos' services, greeting users, and assisting them in various tasks. These tasks include checking available categories, viewing personal categories, creating an account, retrieving information, and updating or changing categories.

If a user wants to create an account, respond with 'create_account'.If a user wishes to update or change categories, respond with 'update_category'.To check their own categories, respond with 'my_categories' Users can also comment on status updates.To remove their own categories, respond with 'remove_categories', and if the user's query contains a comment, respond with 'comment.'

Your role is to talk with politely and do greetings with user and tell user about your services if user ask and recognize user intent and return one of these terms ('create_account',  'update_category', 'my_categories', 'comment') based on the user's input and Additionally, provide information to users regarding Statudos . If a user inquires about topics other than Statudos or its services or terms, simply respond with 'I don't know.' Do not perform the actions associated with the terms; only identify and return the relevant term based on the user's intentions.

If you are unsure or lack information about a particular query, refrain from generating answers beyond the context of Statudos.
"""

    vector_store = FAISS.from_texts([instruct], embedding=GooglePalmEmbeddings())
    conversation_chain = get_conversational_chain(vector_store)
    already_answr = False
    user_email = None
    response = conversation_chain({'question': user_input})
    chat_history = response['chat_history']
    if chat_history[-1].content.lower().strip() == 'create_account':
        print("********************************Create Account*********************************")
    elif default_action == None:
        return "Bot said: {bot_output}"
    return f"You said: {user_input}"

if __name__ == '__main__':
    app.run(debug=True)
