from enum import Enum

class ModelList(Enum):
    LLAMA = 'llama'
    GEMMA = 'gemma'


model_list_string = {
    ModelList.LLAMA: "unsloth/Meta-Llama-3.1-8B-Instruct-bnb-4bit",
    ModelList.GEMMA: "google/gemma-3-4b-it"
}