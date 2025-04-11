

def read_prompt_from_file():
    file_path = 'promptIO/input.txt'
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


def write_output_to_file(output_text):
    with open('promptIO/output.txt', 'w', encoding='utf-8') as file:
        file.write(output_text)