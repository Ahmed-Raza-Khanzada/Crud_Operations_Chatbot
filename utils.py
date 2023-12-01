import re

from call_data_apis import call_get_email_api,get_category_data
def find_email(input_string):
   
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    match = re.search(email_pattern, input_string)
    if match:
        return match.group()
    else:
        return None
def check_email_validity(user_answer):
    email = None
    r = find_email(user_answer)
    if r!=None:
        response1 = f"Bot: is this email is correct or not?\n{r}\nPlease only answer in 'yes' or 'no'"
        print(response1+"\n"+"-"*10)
        user_answer = input("You: ")
        if user_answer.strip().lower() == 'yes':
            user_email = r
            email = r
            action = "break"
        elif user_answer.strip().lower() == 'no':
            action ="continue"
        else:
            already_answr = True
            action = "break"
        return email,already_answr,action
    else:
        return email,False,"continue"

def check_email(email):
    email_to_check = email
    exists_status = call_get_email_api(email_to_check)
    categories = {}
    if exists_status.get('message')!='user with this email not found':    
        for c in exists_status.get("data").get("categories"):
            # print("Category:", c.get("name"),"               Id:", c.get("id"))
            categories[c.get("name").lower().strip()] = c.get("id")
        return True,categories
    return False,categories
def get_availaible_categories():
    api_url = 'http://192.168.1.103:5000/category/read'
    category_data = get_category_data(api_url)
    categories = {}
    if category_data is not None:
        # print("Category Data:", category_data)
        for c in category_data.get("data").get("categories"):
    
            categories[c.get("name").lower()] = c.get("id")
        categories_names = ",".join(list(categories.keys()))
    else:
        categories_names = "music,information, entertainment,technology"
    return categories_names,categories