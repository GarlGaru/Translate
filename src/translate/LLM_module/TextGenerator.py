from enum import Enum

from src.translate.utils import FileIO
from . import autotransformers
from . import printout
from . import CppBase

class ModelList(Enum):
    LLAMA = 'llama'
    GEMMA = 'gemma'

model_list_string = {
    ModelList.LLAMA: lambda prompt: autotransformers.use_llama(prompt),
    ModelList.GEMMA: lambda prompt: autotransformers.use_gemma(prompt)
}

def start():
    prompt = FileIO.read_prompt_from_file()
    printout.c_out("\nUsing this prompt : ")
    print(prompt)

    printout.c_out("\n ***** Starting Text Generation ***** ")
    generated_text = start_with_select_model(prompt)

    printout.c_out("\n\nGenerated text is : ")
    print(generated_text)
    printout.c_out("\n ***** Text Generation Done ***** ")

    FileIO.write_output_to_file(generated_text)
    printout.c_out("Output is written in file")


def start_with_select_model(prompt):
    selected = FileIO.read_selected_model()
    printout.c_out(f"Selected model : {selected}")

    model_path = FileIO.find_llm_model(selected)
    printout.c_out(f"find out model : {model_path}")
    return CppBase.use_llama_cpp(model_path, prompt)


#deprecated
def model_handler(model_name:str, prompt:str):
    try:
        enum_model = ModelList.__members__.get(model_name.upper())
    except KeyError:
        raise ValueError(f"Unknown model name  {model_name}")

    return model_list_string[enum_model](prompt)
