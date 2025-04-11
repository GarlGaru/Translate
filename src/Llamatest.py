# import transformers
# import torch
# import ast
import FileIO

from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

def start():
    model_id = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        trust_remote_code=True
    )

    prompt = FileIO.read_prompt_from_file()

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    streamer = TextStreamer(tokenizer)

    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        do_sample=True,       # 샘플링 활성화
        top_k=50,             # 상위 50개 후보 중 샘플링
        top_p=0.95,           # 누적 확률이 95%인 후보 중 샘플링
        temperature=0.7,      # 온도 조절로 출력의 무작위성 조절
        repetition_penalty=1.2 # 반복 패턴에 대한 패널티 부여
    )

    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    FileIO.write_output_to_file(generated_text)

start()