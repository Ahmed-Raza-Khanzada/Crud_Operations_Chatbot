from flask import Flask, render_template, request

app = Flask(__name__)

# Define a function to generate bot responses
def get_bot_response(user_answer):
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
    while True:
        if not already_answr:
            user_answer = input("You: ")

        
        if user_answer.lower() == 'exit':
            response1 = "Bot: Goodbye! Have a great day."
            print(response1+"\n"+"-"*10)
            break
        already_answr = False
        # Process user input and get the bot's response
        response = conversation_chain({'question': user_answer})
        chat_history = response['chat_history']

        # print("CHat Historrrrrrrrrrrrrrrry")
        # print(chat_history)
        if chat_history[-1].content.lower().strip() == 'create_account':
            print("********************************Create Account*********************************")

            print(chat_history[-1].content.lower().strip(),"Entered in Manual Bot")
            flag,record_reponse_create_account = Create_Account(categories_names=categories_names,categories=categories)
            # print("**********",record_reponse_create_account)
            if flag:
                continue
            else:
                response1 = "Bot: Thank you for using statudos"
                print(response1+"\n"+"-"*10)
                break
        elif chat_history[-1].content.lower().strip() == 'update_category':
            print("********************************Update Categories*********************************")
            if user_email==None:
                while True:
                    response1 = "Bot: To update your categories please provide your email?"
                    print(response1+"\n"+"-"*10)
                    user_answer = input("You: ")
                    email = None
                    r = find_email(user_answer)
                    if r!=None:
                        response1 = f"Bot: is this email is correct or not?\n{r}\nPlease only answer in 'yes' or 'no'"
                        print(response1+"\n"+"-"*10)
                        user_answer = input("You: ")
                        if user_answer.strip().lower() == 'yes':
                            user_email = r
                            email = r
                            break
                        elif user_answer.strip().lower() == 'no':
                            continue
                        else:
                            already_answr = True
                            break
                    
            else:
                email = user_email
            if email!= None:
                res = check_email(email)
                if res[0]==True:
                    avail_category= list(res[1].keys())
                    
                    response1 = f"Bot: your categories are {','.join(avail_category)}\nDo you want to update your categories?\nplease only answer in 'yes' or 'no'"
                    print(response1+"\n"+"-"*10)

                    user_answer = input("You: ")
                    if user_answer=="yes":
                        response1 = f"Bot: Please provide your new categories?\nAvailable categories are {categories_names}"
                        print(response1+"\n"+"-"*10)
                        user_answer = input("You: ")
                        user_account_cats = []
                        for cat in categories_names.split(","):
                            if cat.lower().strip() in user_answer.lower().strip():
                                user_account_cats.append(categories[cat.lower().strip()])
                        if len(user_account_cats)>0:    
                            update_res = remove_update_category_api({'email':email,'categories':user_account_cats})
                            if update_res.get("message")!="categories with this id not found":
                                response1 = "Bot: Your Account Categories are updated"
                                print(response1+"\n"+"-"*10)
                                if update_res.get("data").get("nonExistingCategories"):
                                    response1 = f"Bot: These categories are not available: {','.join(update_res.get('data').get('nonExistingCategories'))}\nAvailable categories are: {categories_names}"
                                    print(response1+"\n"+"-"*10)
                            elif update_res.get("message")=="categories with this id not found":
                                response1 = f"Bot: {update_res.get('message')}"
                                print(response1+"\n"+"-"*10)
                            else:
                                response1 = "Bot: Failed to update your categories"
                                print(response1+"\n"+"-"*10)
                        else:
                            already_answr = True
                        print("Your Account Categories are updated")
                    elif user_answer=="no":
                        response1 = "Bot: So how may i help you now?"
                        print(response1+"\n"+"-"*10)
                    elif user_answer.strip().lower() == 'exit':
                        response1 = "Bot: Goodbye! Have a great day."
                        print(response1+"\n"+"-"*10)
                        break
                    else:
                        already_answr = True
                else:
                    response1 = f"Bot: Sorry there is no Account with this email: {email}\n if you want to create an account type create_account"
                    print(response1+"\n"+"-"*10)
            else:
                already_answr = True
        elif chat_history[-1].content.lower().strip() == 'my_categories':
            print("********************************My Categories*********************************")
            if user_email==None:
                while True:
                    response1 = "Bot: To update your categories please provide your email?"
                    print(response1+"\n"+"-"*10)
                    user_answer = input("You: ")
                    email = None
                    r = find_email(user_answer)
                    if r!=None:
                        response1 = f"Bot: is this email is correct or not?\n{r}\nPlease only answer in 'yes' or 'no'"
                        print(response1+"\n"+"-"*10)
                        user_answer = input("You: ")
                        if user_answer.strip().lower() == 'yes':
                            user_email = r
                            email = r
                            break
                        elif user_answer.strip().lower() == 'no':
                            continue
                        else:
                            already_answr = True
                            break
            else:
                email = user_email

            if email!= None:
                res = check_email(email)
                if res[0]==True:
                    avail_category= list(res[1].keys())
                   
                    print(avail_category)
                    response1 = f"Bot: your categories are {','.join(avail_category)}"
                    print(response1+"\n"+"-"*10)

                else:
                    response1 = f"Bot: Sorry there is no Account with this email: {email}\n if you want to create an account type 'I want to create_account'"
                    print(response1+"\n"+"-"*10)
            else:
                already_answr = True
        elif chat_history[-1].content.lower().strip() == 'remove_categories':
            print("********************************Remove Categories*********************************")
            if user_email==None:
                while True:
                    response1 = "Bot: To update your categories please provide your email?"
                    print(response1+"\n"+"-"*10)
                    user_answer = input("You: ")
                    email = None
                    r = find_email(user_answer)
                    if r!=None:
                        response1 = f"Bot: is this email is correct or not?\n{r}\nPlease only answer in 'yes' or 'no'"
                        print(response1+"\n"+"-"*10)
                        user_answer = input("You: ")
                        if user_answer.strip().lower() == 'yes':
                            user_email = r
                            email = r
                            break
                        elif user_answer.strip().lower() == 'no':
                            continue
                        else:
                            already_answr = True
                            break
            else:
                email = user_email

            if email!= None:
                res = check_email(email)
                if res[0]==True:
                    avail_category= list(res[1].keys())
                    response1 = f"Bot: your categories are {','.join(avail_category)}\nwhich categories you want to remove?"
                    print(response1+"\n"+"-"*10)
                    user_answer = input("You: ")
                    user_account_cats = []
                    for cat in user_answer.split(","):
                        if cat.lower().strip() in avail_category:
                            user_account_cats.append(categories[cat.lower().strip()])
                    if len(user_account_cats)>0:
                        remove_res = remove_update_category_api({'email':email,'categories':user_account_cats},remove=True)
                        if remove_res.get("message")!="categories with this id not found":
                            response1 = "Bot: Your Account Categories are removed"
                            print(response1+"\n"+"-"*10)
                            if remove_res.get("data").get("nonExistingCategories"):
                                response1 = f"Bot: These categories are not available: {','.join(remove_res.get('data').get('nonExistingCategories'))}\nAvailable categories are: {categories_names}"
                                print(response1+"\n"+"-"*10)
                        elif remove_res.get("message")=="categories with this id not found":
                            response1 = f"Bot: {remove_res.get('message')}"
                            print(response1+"\n"+"-"*10)
                        else:
                            response1 = "Bot: Failed to remove your categories"
                            print(response1+"\n"+"-"*10)
                else:
                    response1 = f"Bot: Sorry there is no Account with this email: {email}\n if you want to create an account type 'I want to create_account'"
                    print(response1+"\n"+"-"*10)
            
        else:
            print("Bot:", chat_history[-1].content+"\n"+"-"*10)
    return f"You said: {response1}"

# Define the route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Define the route for handling user input and displaying bot responses
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    bot_response = get_bot_response(user_input)
    return render_template('index.html', user_input=user_input, bot_response=bot_response)

if __name__ == '__main__':
    app.run(debug=True)
