from src.translate.utils import FileIO
from . import autotransformers
from . import printout

def start():

    prompt = FileIO.read_prompt_from_file()
    printout.c_out("\nUsing this prompt : ")
    print(prompt)

    printout.c_out("\n ***** Starting Text Generation ***** ")
    generated_text = autotransformers.use_llama(prompt)

    printout.c_out("\n\nGenerated text is : ")
    print(generated_text)
    printout.c_out("\n ***** Text Generation Done ***** ")

    FileIO.write_output_to_file(generated_text)
    printout.c_out("Output is written in file")
