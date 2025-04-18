from pathlib import Path
import difflib

src_dir = Path(__file__).resolve().parent.parent.parent

def read_prompt_from_file():
    input_path = src_dir / 'promptIO' / 'input.txt'
    with open(input_path, 'r', encoding='utf-8') as file:
        input_str = file.read()

    marker = "############input_start_here############"
    start_index = input_str.find(marker)
    if start_index == -1:
        return input_str
    else:
        return input_str[start_index + len(marker):].lstrip()


def write_output_to_file(output_text):
    output_path = src_dir / 'promptIO' / 'output.txt'
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(output_text)

def read_selected_model():
    file_path = src_dir / 'promptIO' / 'selected_model.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


project_dir = src_dir.parent
llm_models_dir = project_dir / 'LLM_models'

def find_llm_model(name: str):
    files = list(llm_models_dir.glob('*'))
    file_names = [f.name for f in files if f.is_file()]

    matches = difflib.get_close_matches(name, file_names, n=1, cutoff=0.3)

    if matches:
        return str(llm_models_dir / matches[0])
    else:
        return None
