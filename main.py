from langchain.llms import GooglePalm
from langchain.embeddings import GooglePalmEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ChatMessageHistory
from call_data_apis import create_user_api, check_email
from utils import find_email, get_availaible_categories

import os
import re

os.environ['GOOGLE_API_KEY'] = 'AIzaSyAJuIFT_1XfowTRQH_qP5VC9ip8VTdyNKs'


def ask_anything():
    flag2 = False
    while True:
        response1 = "Bot: Is there anything else I can help you with?\nPlease only answer in 'yes' or 'no'"
        print(response1 + "\n" + "-" * 10)
        user_answer = input("You: ")
        if user_answer.strip().lower() == 'yes':
            response1 = "Bot: What can I help you with?"
            print(response1 + "\n" + "-" * 10)
            flag2 = True
            break
        elif user_answer.strip().lower() == 'no':
            response1 = "Bot: Thank you for using Statudos"
            print(response1 + "\n" + "-" * 10)
            break
        else:
            response1 = "Bot: Sorry, I don't understand"
            print(response1 + "\n" + "-" * 10)
            continue
    return flag2


def Create_Account():
    record_response_create_account = {"name": None, "email": None, "categories": None}
    force_exit = False
    while record_response_create_account["name"] is None or record_response_create_account["email"] is None or \
            record_response_create_account["categories"] is None:
        flag = False
        questions = ["What is your name?", "What is your email?", "What are your categories?"]
        while True:
            for pos, q in enumerate(questions):
                if record_response_create_account["name"] is not None and \
                        questions[pos].split(" ")[-1][:-1] == "name":
                    continue
                if record_response_create_account["email"] is not None and \
                        questions[pos].split(" ")[-1][:-1] == "email":
                    continue
                if record_response_create_account["categories"] is not None and \
                        questions[pos].split(" ")[-1][:-1] == "categories":
                    continue
                response1 = f"Bot: {q}"
                print(response1 + "\n" + "-" * 10)
                user_answer = input("You: ")
                if user_answer.strip().lower() == 'exit':
                    force_exit = True
                    break
                if questions[pos].split(" ")[-1][:-1] == "name":
                    record_response_create_account["name"] = user_answer
                elif questions[pos].split(" ")[-1][:-1] == "email":
                    record_response_create_account["email"] = user_answer
                elif questions[pos].split(" ")[-1][:-1] == "categories":
                    record_response_create_account["categories"] = user_answer

            while True:
                if record_response_create_account["name"] is not None and \
                        record_response_create_account["email"] is not None and \
                        record_response_create_account["categories"] is not None:
                    response1 = f"Bot: Is the given information correct?\nName: {record_response_create_account['name']}\nEmail: {record_response_create_account['email']}\nCategories: {record_response_create_account['categories']}\nPlease only answer in 'yes' or 'no' (if you want to exit, type 'exit')"
                    print(response1 + "\n" + "-" * 10)
                    user_answer = input("You: ")
                    if user_answer.strip().lower() == 'yes':
                        flag = True
                        break
                    elif user_answer.strip().lower() == 'no':
                        my_flag = False
                        response1 = "Bot: What is wrong?\nPlease only answer in 'name' or 'email' or 'categories' or 'exit'\nE.g., name\nor\nname,email\nor\nname,email,categories\nor\nexit"
                        print(response1 + "\n" + "-" * 10)
                        while True:
                            user_answer = input("You: ")
                            if user_answer.strip().lower() == 'exit':
                                force_exit = True
                                flag = True
                                my_flag = True
                                break
                            elif "name" in user_answer.strip().lower() and "email" in user_answer.strip().lower() and "categories" in user_answer.strip().lower():
                                record_response_create_account["name"] = None
                                record_response_create_account["email"] = None
                                record_response_create_account["categories"] = None
                                my_flag = True
                                break
                            elif "name" in user_answer.strip().lower() and "email" in user_answer.strip().lower():
                                record_response_create_account["name"] = None
                                record_response_create_account["email"] = None
                                my_flag = True
                                break
                            elif "name" in user_answer.strip().lower() and "categories" in user_answer.strip().lower():
                                record_response_create_account["name"] = None
                                record_response_create_account["categories"] = None
                                my_flag = True
                                break
                            elif "email" in user_answer.strip().lower() and "categories" in user_answer.strip().lower():
                                record_response_create_account["email"] = None
                                record_response_create_account["categories"] = None
                                my_flag = True
                                break
                            elif user_answer.strip().lower() == 'name':
                                record_response_create_account["name"] = None
                                my_flag = True
                                break
                            elif user_answer.strip().lower() == 'email':
                                record_response_create_account["email"] = None
                                my_flag = True
                                break
                            elif user_answer.strip().lower() == 'categories':
                                record_response_create_account["categories"] = None
                                my_flag = True
                                break
                            else:
                                response1 = "Bot: Sorry, I don't understand"
                                print(response1 + "\n" + "-" * 10)
                                continue
                        if my_flag:
                            break
                    elif user_answer.strip().lower() == 'exit':
                        force_exit = True
                        flag = True
                        break
                    else:
                        response1 = "Bot: Sorry, I don't understand"
                        print(response1 + "\n" + "-" * 10)
                        continue
            if flag:
                break

    if force_exit is False and (
            record_response_create_account["name"] is not None and
            record_response_create_account["email"] is not None and
            record_response_create_account["categories"] is not None):

        user_account_cats = []
        not_avail_categories = []
        for user_cat in record_response_create_account["categories"].split(","):
            if user_cat.lower().strip() in categories.keys():
                user_account_cats.append(categories[user_cat.lower().strip()])
            else:
                not_avail_categories.append(user_cat.lower().strip())
        if len(not_avail_categories) > 0:
            response1 = f"Bot: Sorry, these categories are not available: {','.join(not_avail_categories)}\nAvailable categories are {categories_names}"
            print(response1 + "\n" + "-" * 10)
        if len(user_account_cats) > 0:
            input_data = {'userName': record_response_create_account["name"],
                          'email': record_response_create_account["email"],
                          'categories': user_account_cats}
            output_data = create_user_api(input_data)
            if output_data is not None:
                if output_data["message"] != "user with this email already exists":
                    response1 = "Bot: Thank you for creating an account"
                    print(response1 + "\n" + "-" * 10)
                    response1 = "Bot: Your account has been created successfully"
                    print(response1 + "\n" + "-" * 10)
                elif output_data["message"] == "user with this email already exists":
                    response1 = "Bot: User with this email already exists"
                    print(response1 + "\n" + "-" * 10)
                else:
                    response1 = "Bot: Failed to create an account"
                    print(response1 + "\n" + "-" * 10)
            else:
                response1 = "Bot: Failed to create an account"
                print(response1 + "\n" + "-" * 10)

        flag2 = ask_anything()
        return flag2, record_response_create_account

    if flag2:
        flag2 = ask_anything()
        return flag2, record_response_create_account

    return False, record_response_create_account


def get_conversational_chain(vector_store):
    llm = GooglePalm()

    # Set up a system message to start the conversation
    system_message = "Hi, I am Statudos Bot. How can I help you today?"

    memory = ChatMessageHistory()
    conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(),
                                                               memory=memory)
    # Start the conversation with the system message
    conversation_chain({'question': system_message})

    return conversation_chain

from langchain.llms import GooglePalm
from langchain.embeddings import GooglePalmEmbeddings
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch

class ChatMessageHistory:
    def __init__(self):
        self.messages = []

    def add_user_message(self, content):
        self.messages.append(HumanMessage(content=content, additional_kwargs={}))

    def get_response_from_class(self, predicted_class):
        # You need to implement this method based on your specific use case
        pass

class HumanMessage:
    def __init__(self, content, additional_kwargs):
        self.content = content
        self.additional_kwargs = additional_kwargs

def update_and_generate_response(history, user_message):
    # Instructions for PALM-2 before chatting with the user
    categories_names = ["category1", "category2", "category3"]  # Replace with actual category names
    instruct = f"""Statudos is a website providing information about influencers and their status based on personal categories ({categories_names}). You are a Statudos WhatsApp bot with the role of offering details about Statudos' services, greeting users, and assisting them in various tasks. These tasks include checking available categories, viewing personal categories, creating an account, retrieving information, and updating or changing categories.

If a user wants to create an account, respond with 'create_account.' For checking available categories, respond with 'check_categories.' If a user wishes to update or change categories, respond with 'update_category.' To check their own categories, respond with 'my_categories.' Users can also comment on status updates, and if the user's query contains a comment, respond with 'comment.'

Your role is to talk with users (do greetings) politely and recognize user intent and return one of these terms ('create_account', 'check_categories', 'update_category', 'my_categories', 'comment') based on the user's input. Additionally, provide information to users regarding Statudos. If a user inquires about topics other than Statudos or its services or terms, simply respond with 'I don't know.' Do not perform the actions associated with the terms; only identify and return the relevant term based on the user's intentions.

If you are unsure or lack information about a particular query, refrain from generating answers beyond the context of Statudos.
"""
    print(instruct)

    # Initialize PALM-2 model
    palm_model_name = "google/palm-2-large-turbo"
    palm_model = GooglePalm.from_pretrained(palm_model_name)
    tokenizer = AutoTokenizer.from_pretrained(palm_model_name)

    # Update chat history with the user message
    history.add_user_message(user_message)

    # Encode the conversation
    conversation = [message.content for message in history.messages]
    inputs = tokenizer(conversation, return_tensors="pt", truncation=True, padding=True)

    # Make prediction using PALM-2
    outputs = palm_model(**inputs)
    probabilities = outputs.logits.softmax(dim=-1)
    predicted_class = torch.argmax(probabilities, dim=-1).item()

    # Get response from class (you need to implement this method in your ChatMessageHistory class)
    response = history.get_response_from_class(predicted_class)

    return response

# Example usage
history = ChatMessageHistory()
user_message = "How are you doing?"
response = update_and_generate_response(history, user_message)
print(response)





def chat_with_palm2():
    categories_names, categories = get_availaible_categories()
    print("Type 'exit' to end the conversation.")
    instruct = f"""Statudos is a website providing information about influencers and their status based on personal categories ({categories_names}). You are a Statudos WhatsApp bot with the role of offering details about Statudos' services, greeting users, and assisting them in various tasks. These tasks include checking available categories, viewing personal categories, creating an account, retrieving information, and updating or changing categories.

If a user wants to create an account, respond with 'create_account.' For checking available categories, respond with 'check_categories.' If a user wishes to update or change categories, respond with 'update_category.' To check their own categories, respond with 'my_categories.' Users can also comment on status updates, and if the user's query contains a comment, respond with 'comment.'

Your role is to talk with users (do greetings) politely and recognize user intent and return one of these terms ('create_account', 'check_categories', 'update_category', 'my_categories', 'comment') based on the user's input. Additionally, provide information to users regarding Statudos. If a user inquires about topics other than Statudos or its services or terms, simply respond with 'I don't know.' Do not perform the actions associated with the terms; only identify and return the relevant term based on the user's intentions.

If you are unsure or lack information about a particular query, refrain from generating answers beyond the context of Statudos.
"""

    vector_store = FAISS.from_texts([instruct], embedding=GooglePalmEmbeddings())
    conversation_chain = get_conversational_chain(vector_store)
    already_answered = False

    while True:
        if not already_answered:
            user_answer = input("You: ")

        if user_answer.lower() == 'exit':
            response1 = "Bot: Goodbye! Have a great day."
            print(response1 + "\n" + "-" * 10)
            break
        already_answered = False

        # Process user input and get the bot's response
        conversation_chain({'question': user_answer})
        chat_history = conversation_chain.memory.get_all_messages()

        if chat_history[-1].content.lower().strip() == 'create_account':
            print("********************************Create Account*********************************")
            print(chat_history[-1].content.lower().strip(), "Entered in Manual Bot")
            flag, record_response_create_account = Create_Account()

            if flag:
                continue
            else:
                response1 = "Bot: Thank you for using Statudos"
                print(response1 + "\n" + "-" * 10)
                break
        elif chat_history[-1].content.lower().strip() == 'update_category':
            print("********************************Update Categories*********************************")
            response1 = "Bot: To update your categories please provide your email?"
            print(response1 + "\n" + "-" * 10)
            user_answer = input("You: ")
            email = None
            r = find_email(user_answer)
            if r is not None:
                email = r
            if email is not None:
                res = check_email(email)
                if res[0] is True:
                    avail_category = list(res[1].keys())

                    response1 = f"Bot: Your categories are {','.join(avail_category)}\nDo you want to update your categories?\nPlease only answer in 'yes' or 'no'"
                    print(response1 + "\n" + "-" * 10)
                    print("Your Account Categories are updated")
                else:
                    response1 = f"Bot: Sorry, there is no account with this email: {email}\n If you want to create an account type 'create_account'"
                    print(response1 + "\n" + "-" * 10)
            else:
                already_answered = True
        elif chat_history[-1].content.lower().strip() == 'my_categories':
            print("********************************My Categories*********************************")
            response1 = "Bot: To check your categories please provide your email?"
            print(response1 + "\n" + "-" * 10)
            user_answer = input("You: ")

            r = find_email(user_answer)
            email = None
            if r is not None:
                email = r

            if email is not None:
                res = check_email(email)
                if res[0] is True:
                    avail_category = list(res[1].keys())

                    print(avail_category)
                    response1 = f"Bot: Your categories are {','.join(avail_category)}"
                    print(response1 + "\n" + "-" * 10)

                else:
                    response1 = f"Bot: Sorry, there is no account with this email: {email}\n If you want to create an account type 'I want to create_account'"
                    print(response1 + "\n" + "-" * 10)
            else:
                already_answered
