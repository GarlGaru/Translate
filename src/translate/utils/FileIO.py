from pathlib import Path

src_dir = Path(__file__).resolve().parent.parent.parent

def read_prompt_from_file():
    input_path = src_dir / 'promptIO' / 'input.txt'
    with open(input_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_output_to_file(output_text):
    output_path = src_dir / 'promptIO' / 'output.txt'
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(output_text)