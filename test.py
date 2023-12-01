
# from langchain import TextMessage, Conversation
from langchain.llms import GooglePalm
from langchain.embeddings import GooglePalmEmbeddings
from langchain.vectorstores import FAISS
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain

import os

os.environ['GOOGLE_API_KEY'] =  'AIzaSyAJuIFT_1XfowTRQH_qP5VC9ip8VTdyNKs'


def create_chat(vector_store, conversation_chain=None):
    instruct = """Statudos is a website providing information about influencers and their status based on personal categories ({categories_names}). You are a Statudos WhatsApp bot with the role of offering details about Statudos' services, greeting users, and assisting them in various tasks. These tasks include checking available categories, viewing personal categories, creating an account, retrieving information, and updating or changing categories.

If a user wants to create an account, respond with 'create_account.' For checking available categories, respond with 'check_categories.' If a user wishes to update or change categories, respond with 'update_category.' To check their own categories, respond with 'my_categories.' Users can also comment on status updates, and if the user's query contains a comment, respond with 'comment.'

Your role is to talk with users (do greetings) politely and recognize user intent and return one of these terms ('create_account', 'check_categories', 'update_category', 'my_categories', 'comment') based on the user's input. Additionally, provide information to users regarding Statudos. If a user inquires about topics other than Statudos or its services or terms, simply respond with 'I don't know.' Do not perform the actions associated with the terms; only identify and return the relevant term based on the user's intentions.

If you are unsure or lack information about a particular query, refrain from generating answers beyond the context of Statudos.
"""

    if conversation_chain is None:
        llm = GooglePalm()
        
        # Set up a system message to start the conversation
        system_message = "Hi I am statudos Bot, How can i help you today?"
        
        memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
        conversation_chain = ConversationalRetrievalChain.from_llm(llm=llm, retriever=vector_store.as_retriever(), memory=memory)
        # Start the conversation with the system message and instructions
        conversation_chain({'question': system_message})
        conversation_chain({'instruction': instruct})

    def chat(user_question):
        # Add user question to the conversation
        conversation_chain({'question': user_question})

        # Get the bot's response
        bot_response = conversation_chain()

        # Update conversation history with the latest user and bot messages
        user_message = TextMessage(user_question)
        bot_message = TextMessage(bot_response['answer'])
        conversation = Conversation(messages=[user_message, bot_message])

        # Update conversation history in memory
        conversation_chain.memory.add(conversation)

        return bot_response['answer']

    return chat, conversation_chain


instruct = f"""Statudos is a website providing information about influencers and their status based on personal categories ({categories_names}). You are a Statudos WhatsApp bot with the role of offering details about Statudos' services, greeting users, and assisting them in various tasks. These tasks include checking available categories, viewing personal categories, creating an account, retrieving information, and updating or changing categories.

If a user wants to create an account, respond with 'create_account.' For checking available categories, respond with 'check_categories.' If a user wishes to update or change categories, respond with 'update_category.' To check their own categories, respond with 'my_categories.' Users can also comment on status updates, and if the user's query contains a comment, respond with 'comment.'

Your role is to talk with users(do greetings) politely and recognize user intent and return one of these terms ('create_account', 'check_categories', 'update_category', 'my_categories', 'comment') based on the user's input and Additionally, provide information to users regarding Statudos . If a user inquires about topics other than Statudos or its services or terms, simply respond with 'I don't know.' Do not perform the actions associated with the terms; only identify and return the relevant term based on the user's intentions.

If you are unsure or lack information about a particular query, refrain from generating answers beyond the context of Statudos.
"""


vector_store = FAISS.from_texts([instruct], embedding=GooglePalmEmbeddings())
chat_function, conversation_chain = create_chat(vector_store)

# Example conversation
user_question_1 = "How do I create an account?"
bot_response_1 = chat_function(user_question_1)
print(bot_response_1)

user_question_2 = "What categories are available?"
bot_response_2 = chat_function(user_question_2)
print(bot_response_2)



