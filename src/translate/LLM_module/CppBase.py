import inspect
from llama_cpp import Llama

def use_llama_cpp(model_path_str, prompt):

    llm = Llama(
        model_path=model_path_str,
        n_ctx=5128,
        n_batch=1024,    #default=512
        n_gpu_layers=-1,
        logits_all=False,
        vocab_only=False,
        verbose=False
    )


    output = llm(
        prompt,
        top_p=0.95,         #default=0.95
        max_tokens=2048,     #default=16
        temperature=0.7,     #default=0.8
        top_k=50,           #default=40
        repeat_penalty=1.2,     #default=1.0
        stream = False,     #default=False
        echo=False          #default=False
    )
    # print(output)

    return output["choices"][0]["text"].strip()

# {
#     'id': 'cmpl-uuid',
#     'object': 'text_completion',
#     'created': 1234567890,
#     'model': '\\LLM_models\\gemma-3-4b-it-q4_0.gguf',
#     'choices': [
#         {
#             'text': '\n저는 챗봇입니다.\n\n궁금한 점이 있다면 언제든지 물어보세요! 😊\n',
#             'index': 0, 'logprobs': None,
#             'finish_reason': 'stop'
#         }
#     ],
#     'usage': {
#         'prompt_tokens': 4,
#         'completion_tokens': 23,
#         'total_tokens': 27
#     }
# }
