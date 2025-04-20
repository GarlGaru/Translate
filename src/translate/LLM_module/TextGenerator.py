from enum import Enum

from src.translate.utils import FileIO
from . import Autotransformers
from . import Printout
from . import CppBase
from . import TokenSplitter

# translated = "만약 태양 돛을 사용한다면, 수 킬로미터 길이의 반사면은 엄청난 양의 빛을 담고 있으며, 이를 집중된 형태로 활용하여 광합성이나 태양 전지판을 작동시키기 꽤 쉽습니다. 심지어 플루토 너머의 척박한 성간 공간에서도 저기술의 우주선은 약간 더 어렵습니다. 왜냐하면 태양은 성간 공간에서 이용할 수 없기 때문입니다. 따라서 전력과 추진력을 위해 핵 옵션을 고려해야 합니다. 하지만 수십 년에서 수 세기 동안 반감기를 갖는 방사성 동위원소를 사용하면 매우 저기술적인 전력 공급원이 됩니다. 일반적으로 열전쌍과 연결하여 Seebeck 효과, 즉 토마스 Seebeck이 1821년에 발견한 과정을 통해 전기를 생산합니다. 이는 200년 전에 발견된 기술이므로 매우 저기술적인 방법입니다."
translated = "태양 돛을 사용한다면 수 킬로미터에 달하는 반사 돛은 막대한 빛을 받아 그 일부를 집중시켜 광합성이나 태양 전지판을 구동하기가 꽤 쉽고, 심지어 명왕성 너머에서도 가능하지만 저기술 성간 우주선은 좀 더 까다롭습니다. 성간 공간에서는 태양을 실질적으로 이용할 수 없으므로 동력과 추진을 위해 핵 옵션을 고려해야 하며, 반감기가 수십 년에서 수세기에 이르는 방사성 동위원소가 있다면 그것은 매우 저기술적인 전력 공급원이 될 수 있습니다. 우리는 보통 이를 지벡 효과에 따라 전력을 생산하도록 열전대에 연결하는데, 이 과정은 1821년 토머스 지벡이 200년 전에 발견한 것으로 결코 첨단 기술이 아닙니다."
origin_text = ["Though if you are using solar sails, kilometers worth of reflective sail is a lot of light",
"and it is pretty easy to divert a bit of that into concentrated form to be running photosynthesis",
"or solar panels, even out past Pluto, low-tech interstellar ships are a bit harder, because",
"the sun really isn't available in interstellar space, so you need be considering nuclear options",
"for power and drives, but if you've got some radioisotopes with decades to centuries",
"for a half-life that is a very low-tech power supply, we normally hook it up to a thermocouple",
"to make power, such as by the Seebeck Effect, which is hardly high-tech since Thomas Seebeck",
"discovered the process 200 years ago in 1821."]

def start():
    if True:
        split= TokenSplitter.consume_with_tokenizer(origin_text, translated)
        for s in split:
            print(s)
        return 
    
    prompt = FileIO.read_prompt_from_file()
    Printout.c_out("\nUsing this prompt : ")
    print(prompt)

    Printout.c_out("\n ***** Starting Text Generation ***** ")
    generated_text = start_with_select_model(prompt)

    Printout.c_out("\n\nGenerated text is : ")
    print(generated_text)
    Printout.c_out("\n ***** Text Generation Done ***** ")

    FileIO.write_output_to_file(generated_text)
    Printout.c_out("Output is written in file")


def start_with_select_model(prompt):
    selected = FileIO.read_selected_model()
    Printout.c_out(f"Selected model : {selected}")

    model_path = FileIO.find_llm_model(selected)
    Printout.c_out(f"find out model : {model_path}")
    return CppBase.use_llama_cpp(model_path, prompt)




#deprecated
class ModelList(Enum):
    LLAMA = 'llama'
    GEMMA = 'gemma'

model_list_string = {
    ModelList.LLAMA: lambda prompt: Autotransformers.use_llama(prompt),
    ModelList.GEMMA: lambda prompt: Autotransformers.use_gemma(prompt)
}
def model_handler(model_name:str, prompt:str):
    try:
        enum_model = ModelList.__members__.get(model_name.upper())
    except KeyError:
        raise ValueError(f"Unknown model name  {model_name}")

    return model_list_string[enum_model](prompt)
