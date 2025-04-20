from . import Printout
from transformers import AutoTokenizer, AutoModelForCausalLM


def use_llama(prompt):
    # model_id = "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit"
    model_id = "google/gemma-3-4b-it"
    Printout.m_out(model_id)

    tokenizer = AutoTokenizer.from_pretrained(model_id)

    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        device_map="auto",
        trust_remote_code=True
    )


    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    outputs = model.generate(
        **inputs,
        max_new_tokens=1000,
        do_sample=True,       # 샘플링 활성화
        top_k=40,             # 상위 ~개 후보 중 샘플링
        top_p=0.85,           # 누적 확률이 ~%인 후보 중 샘플링
        temperature=0.6,      # 높을 수록 창의성
        repetition_penalty=1.1 # 반복 패턴에 대한 패널티 부여
    )


    full_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return full_text[len(prompt):]  #입력 제거 후 리턴


def use_gemma(prompt):
    model_id = "google/gemma-3-4b-it"
    Printout.m_out(model_id)

