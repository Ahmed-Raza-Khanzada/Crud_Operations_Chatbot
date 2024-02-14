import json

def read_jsonl_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Load each line as a JSON object
            json_obj = json.loads(line.strip(),)
            data.append(json_obj)
    return data

#
file_path = 'conversations/chatbotchatend.jsonl'
with open(file_path,"r") as f:
    for line in f:
        print(json.load(f))