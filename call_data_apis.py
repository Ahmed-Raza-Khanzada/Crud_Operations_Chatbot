import requests

def create_user_api(input_data):
    api_url = 'http://192.168.1.103:5000/user/sign-up'

    try:
        response = requests.post(api_url, json=input_data)
        
        output_data = response.json()
        return output_data
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def call_get_email_api(email):
    api_url = f'http://192.168.1.103:5000/user/exists?email={email}'

    try:
        response = requests.get(api_url)
       
        exists_status = response.json()
        return exists_status

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def get_category_data(api_url):
    try:
        response = requests.get(api_url)
        if response.status_code == 200:
            category_data = response.json()
            return category_data
        else:
            print(f"Error: {response.status_code}, {response.text}")
            return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None


def remove_update_category_api(input_data,remove=False):
    if remove:
        api_url = "http://192.168.1.103:5000/user/categories/remove"
    else:
        api_url = "http://192.168.1.103:5000/user/categories/update"
    try:
        response = requests.post(api_url, json=input_data)
        output_data = response.json()
        return output_data
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
# # Example usage with the provided data
# input_data = {'userName': 'Ahmed', 'email': 'kh@gmail.com', 'categories': '[Sports , Entertainment]'}
# output_data = create_user_api(input_data)

# if output_data is not None:
#     print("API Response:", output_data)
# else:
#     print("Failed to call the API.")


# Example usage with a dynamic email
# email_to_check = 'kh@gmail.com'
# exists_status = call_get_email_api(email_to_check)

# if exists_status is not None:
#     print(f"User with email '{email_to_check}' exists: {exists_status.get('message')!='user with this email not found'}")
#     print(exists_status.get("data").get("category"))
# else:
#     print("Failed to call the API.")







# # Example usage with the provided API URL
# api_url = 'http://192.168.1.103:5000/category/read'
# category_data = get_category_data(api_url)
# categories = {}
# if category_data is not None:
#     # print("Category Data:", category_data)
#     for c in category_data.get("data").get("categories"):
#         # print(c)
#         print("Category:", c.get("name"),"               Id:", c.get("id"))
#         categories[c.get("name")] = c.get("id")

   


