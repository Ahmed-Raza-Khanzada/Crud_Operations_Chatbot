from vllm import LLM, SamplingParams
prompts = [
    "Hello, my name is",

]
model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0" 
model_name = "meta-llama/Llama-2-7b-chat-hf"

sampling_params = SamplingParams(temperature=0.8, top_p=0.9)
llm = LLM(model="facebook/opt-125m")

outputs = llm.generate(prompts, sampling_params)

# Print the outputs.
for output in outputs:
    prompt = output.prompt
    generated_text = output.outputs[0].text
    print(f"Prompt: {prompt!r}, Generated text: {generated_text!r}")