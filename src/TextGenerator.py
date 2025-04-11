# import transformers
# import torch
# import ast
import FileIO

from transformers import AutoTokenizer, AutoModelForCausalLM, TextStreamer

def start():

    prompt = FileIO.read_prompt_from_file()
    c_out("\nUsing this prompt : ")
    print(prompt)

    c_out("\n ***** Starting Text Generation ***** ")
    generated_text = use_llama(prompt)

    c_out("\n\nGenerated text is : ")
    print(generated_text)
    c_out("\n ***** Text Generation Done ***** ")

    FileIO.write_output_to_file(generated_text)
    c_out("Output is written in file")


def c_out(text):
    print("\033[32m", text, "\033[0m")

def m_out(model_id):
    print("\033[32m", "\nGenerate Text with :", "\033[0m", "\033[33m", model_id, "\033[0m")


def use_llama(prompt):
    model_id = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"
    m_out(model_id)

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        trust_remote_code=True
    )


    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)


    outputs = model.generate(
        **inputs,
        max_new_tokens=500,
        do_sample=True,       # 샘플링 활성화
        top_k=50,             # 상위 50개 후보 중 샘플링
        top_p=0.95,           # 누적 확률이 95%인 후보 중 샘플링
        temperature=0.7,      # 온도 조절로 출력의 무작위성 조절
        repetition_penalty=1.2 # 반복 패턴에 대한 패널티 부여
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)


def use_gemma(prompt):
    model_id = "google/gemma-3-4b-it"
    m_out(model_id)


