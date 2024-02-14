import json
import logging
import time
from threading import Thread
import torch
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
import requests
import gc
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.llms import Ollama





def give_response(question, model, who="Bot"):
    try:
        final_answer = ""
        print(who + ": ")
        for line in model.stream(question):
            final_answer += line
        print()
        return final_answer

    except Exception as e:
        logging.error(f"Error in generate function: {str(e)}")
        print(e)
        return ""






history2 = ""
chats = 300
chat_length = 15
new_chat = f"\n\n\n\n\n***************************New Chat_0*********************************************"

with open("data_files/My_file_chats_new.txt", "a") as f:
    f.write(new_chat+"\n")
try:
    for chats_iter in range(chats):
        client = Ollama(
            model="Liqclientv17", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
        )
        Chatbot = Ollama(
            model="Liqchatbotv17", callback_manager=CallbackManager([StreamingStdOutCallbackHandler()])
        )
        history = ""
        bot = "Hi there I am LiqChat How may I help you today?"
        history += f"Bot: {bot}"
        with open("data_files/My_file_chats_new.txt", "a") as f:
            f.write(f"Bot: {bot}")
        print("Bot: ",bot)
        
        customer = give_response(bot, client, "Customer")
        history += f"\n\nCustomer: {customer}"
        with open("data_files/My_file_chats_new.txt", "a") as f:
            f.write(f"\n\nCustomer: {customer}")
        new_chat = f"\n\n\n\n\n***************************New Chat_{chats_iter+1}*********************************************"
        for x in range(chat_length):
            bot = give_response(customer, Chatbot, "Bot")
            history += f"\n\nBot: {bot}"
            with open("data_files/My_file_chats_new.txt", "a") as f:
                f.write(f"\n\nBot: {bot}")
            if "<representativie>" in bot:
                break
            customer = give_response(bot, client, "Customer")
            history += f"\n\nCustomer: {customer}"
            with open("data_files/My_file_chats_new.txt", "a") as f:
                f.write(f"\n\nCustomer: {customer}")
            if "chats end" in customer.lower():
                break

        print(new_chat)
        torch.cuda.empty_cache()
        print(chats_iter, "&&&&&&&&&&&&&&&&&&&&Done&&&&&&&&&&&&&&&&&&&&&")
 
        with open("data_files/My_file_chats_new.txt", "a") as f:
            f.write(new_chat+"\n")
        history = ""
        history += new_chat
        
        del client
        del Chatbot
        gc.collect()
except Exception as e:
    print(e)
    print("**********************************************************************")
    with open("data_files/My_file_chats_new_error.txt", "w+") as f:
        f.write(history)
