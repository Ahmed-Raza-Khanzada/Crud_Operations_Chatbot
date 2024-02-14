from torch import cuda, bfloat16, cuda, float32
import transformers
from peft import LoraConfig, PeftModel
import torch
# model_id = 'meta-llama/Llama-2-13b-chat-hf'
# api_key = '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'

def quantization_config():
    if cuda.is_available():
        return transformers.BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_quant_type='nf4',
            bnb_4bit_use_double_quant=True,
            bnb_4bit_compute_dtype=bfloat16
        )
    else:
        return transformers.BitsAndBytesConfig(
            load_in_4bit=False,
            bnb_4bit_quant_type='int8',
            bnb_4bit_use_double_quant=False,
            bnb_4bit_compute_dtype=float32
        )

def model_config(model_id, api_key):
    return transformers.AutoConfig.from_pretrained(
        model_id,
        token = api_key
    )

# def get_model(model_id, api_key):
#     print(f"Model loading on {f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'}...")
#     model = transformers.AutoModelForCausalLM.from_pretrained(
#         model_id,
#         token = api_key,
#         trust_remote_code=True,
#         config=model_config,
#         quantization_config=quantization_config(),
#         device_map='auto',
#         resume_download=False,
#         # device_map={"": 0},
#     )

#     # load_model = AutoModelForCausalLM.from_pretrained(
#     #     base_model,
#     #     # low_cpu_mem_usage=True,
#     #     return_dict=True,
#     #     torch_dtype=torch.float16,
#     #     device_map={"": 0},
#     # )
    # new_model ="/home/osamakhan/Documents/flask_bot/llama2_own_model"
#     model = PeftModel.from_pretrained(model, new_model)
#     model = model.merge_and_unload()
#     return model

def get_model(model_id, api_key=None):
    print(f"Model loading on {f'cuda:{cuda.current_device()}' if cuda.is_available() else 'cpu'}...")
    if api_key is None:
         model = transformers.AutoModelForCausalLM.from_pretrained(
            model_id,
         
            trust_remote_code=True,
           
            quantization_config=quantization_config(),
            device_map='auto',
            resume_download=False,
        )

    else:
        # Load the base model with quantization config
        model = transformers.AutoModelForCausalLM.from_pretrained(
            model_id,
            token=api_key,
            trust_remote_code=True,
            config=model_config,
            quantization_config=quantization_config(),
            device_map='auto',
            resume_download=False,
        )

    # Load the fine-tuned checkpoint
    # model.load_state_dict(torch.load(checkpoint_path))

    # Merge and unload if using LoRA (assuming PeftModel is imported)
    # if model_id.startswith("facebook/llama-"):  # Check for LLaMA models
    new_model = "/home/osamakhan/Documents/flask_bot/mistral-7b-chat-own_datav2"
    new_model ="/home/osamakhan/Documents/flask_bot/llama2_own_modelv4"

    # model = PeftModel.from_pretrained(model, new_model)
    # model = model.merge_and_unload()

    return model

def get_tokenizer(model_id, api_key=None):
    if api_key is None:
        tokenizer = transformers.AutoTokenizer.from_pretrained(
            model_id,
            token = api_key
        )
    else:
        tokenizer = transformers.AutoTokenizer.from_pretrained(
            model_id
        )
    # tokenizer.padding_side = "left"
    # tokenizer.pad_token = tokenizer.eos_token
    # Reload model in FP16 and merge it with LoRA weights

# Reload tokenizer to save it
    # tokenizer = AutoTokenizer.from_pretrained(base_model, trust_remote_code=True)
    tokenizer.add_special_tokens({'pad_token': '[PAD]'})
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"
    return tokenizer
