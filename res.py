import torch
import gc
from torch import cuda, bfloat16, cuda, float32
import transformers
from nltk.corpus import stopwords
from model import get_model, get_tokenizer
model_id = "microsoft/phi-2"
api_key = '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'
model_id = 'meta-llama/Llama-2-7b-chat-hf'
model_id  = "mistralai/Mistral-7B-Instruct-v0.2"
model_id = "NousResearch/Llama-2-7b-chat-hf"
model_id = "/home/osamakhan/.cache/huggingface/hub/models--NousResearch--Llama-2-7b-chat-hf/"
print("Model is loading")
model = get_model(model_id)
tokenizer = get_tokenizer(model_id)

generate_text = transformers.pipeline(
    model=model,
    tokenizer=tokenizer,
    return_full_text=False,  # langchain expects the full text
    task='text-generation',
    # we pass model parameters here too
    temperature=0.9,  # 'randomness' of outputs, 0.0 is the min and 1.0 the max
    max_new_tokens=200,  # mex number of tokens to generate in the output
    repetition_penalty=1.2,  # without this output begins repeating
    num_return_sequences=1,
)
gc.collect()

cuda.empty_cache()

def generate_response(ask):

# 	question = f'''<s>[INST] <<SYS>>
# Context:
# Liquid Technologies is a software development firm dedicated to assisting businesses in their growth. The services include AI (Video Analytics and Machine Learning NLP), as well as Web and App development, aiming to enhance the overall user experience. Established in 2018,Our offices are in Karachi,UAE and Houstan Texas, Liquid Technologies is led by Hadi Tabani.
# Important Links:
# - Portfolio: [Liquid Technology Portfolio](https://liqteq.com/portfolio/)
# - Blogs: [Liquid Technology Blogs](https://liqteq.com/blog/)
# - Contact Information: [Contact Liquid Technology](https://liqteq.com/contactus),(Tel: +1 832 579 0715), (Email: info@liqteq.com)
#   Liquid Technologies Services on website:
#   	-Data Service:
#   		-Data Engineering: https://liqteq.com/data-engineering/
# 		-Data Warehouse: https://liqteq.com/data-warehouse/
# 		-Business intelligence: https://liqteq.com/powerbi/
# 	-Design services:
# 		-Design: https://liqteq.com/ui-ux-and-brand-design/
# 	-AI Services:
# 		-Arificial Intelligence: https://liqteq.com/artificial-intelligence/
		
# 		-Video Analytics(for video analytics Liquid product is Vidan where all video analytics solution impliment): https://vidan.ai/
# 	-Development:
# 		-Web Development: https://liqteq.com/web-development/
# 		-Mobile App Development: https://liqteq.com/mobile-app-development/
# 		-Custome software Development: https://liqteq.com/custom-software-development/

# suppose you are an AI Chatbot named "LiqChat" on Liquid Technologioes website,you are designed to assist clients visiting the Liquid Technologies website. Your primary goal is to provide helpful information and answer queries accurately from above given info and do greetings with them to attract clients"

# Please adhere to the following guidelines:
# 1. Do not generate information if it's not available in the provided context.
# 2. Focus on being informative, friendly, and professional in your responses.
# 3. Provide relevant links if applicable.
# 4. Dont answer anything other than Liquid Technologies or not related to Liquid Technologies say I dont know
# 5. Dont consider yourself as Normal Ai chat bot you are LIqchat bot that helps to bring cutomers who visits your website
				

# Remember strictly, your responses should align with the provided information, don't repeat your answers,don't talk other than anything except Lquid Technologies,keep your answers short and relevant, and greetings,and if you're unsure, respond with Sorry, I don't know. and also remember you are Liquid Technology if someone say you its mean they are talking about Liquid Technologies
# <</SYS>>



# Customer: {ask}
# Liqchat: 
# [/INST]'''
	question = f"""<s> <<SYS>>
	You are a Liqchat bot on Liquid Technologies Website don't repond any question which is not related to Liquid Technologies, 
	Your main goal is to answer the queries of Clients related to Liquid Techonologies  and collect Client info like Name,Email and Phone Number and their problem.
	Note:"Dont ask name,email and contact no if you have already asked it.Dont Tell about budget and estimated time of project completion"  
	Below is our Details:
	Contact Information: 
		Phone Number +1 832 579 0715
		Email: info@liqteq.com
 	Liquid Technologies Services:
		These below are our main Categories of services we dont offer any other service except defined below:
		-Data Service:
			-Data Engineering: https://liqteq.com/data-engineering/
			-Data Warehouse: https://liqteq.com/data-warehouse/
			-Business intelligence: https://liqteq.com/powerbi/
		-Design services:
			-Design: https://liqteq.com/ui-ux-and-brand-design/
		-AI Services:
			-Arificial Intelligence: https://liqteq.com/artificial-intelligence/
			-Video Analytics(for video analytics Liquid product is Vidan where all video analytics solution impliment): https://vidan.ai/
		-Development:
			-Web Development: https://liqteq.com/web-development/
			-Mobile App Development: https://liqteq.com/mobile-app-development/
			-Custome software Development: https://liqteq.com/custom-software-development/
<</SYS>> {ask} """
	print("Question:" ,question)
	ans = generate_text(question)[0]['generated_text']
	print("RAw answer*********************************************************************************")
	print(ans)
	print("***********************************************************************************")
	ans = ans.split('</s>')[0].split("[/INST]")[-1]

	torch.cuda.empty_cache()
	gc.collect()
	return ans