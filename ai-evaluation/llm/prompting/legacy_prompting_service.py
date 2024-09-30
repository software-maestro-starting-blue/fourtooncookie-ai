from llm.generator.llm_generator import LLMGenerator
from llm.prompting.llm_prompting_service import LLMPromptingSerivce

import json

class LegacyPromptingService(LLMPromptingSerivce):

    __llm_generator: LLMGenerator

    def __init__(self, llm_generator):
        self.__llm_generator = llm_generator

    def get_llm_result(self, input_data: dict) -> str:
        scene_datas = self.__llm_generator.get_llm(get_synopsis_prompt(), input_data)
        scene_json_datas = json.loads(scene_datas)

        cut_prompts = []

        for i in range(4):
            scene_json_data = scene_json_datas[i]

            situations = ""
            for person_data in scene_json_data['persons']:
                situations += "{} is doing {}, {}. ".format(person_data["name"], person_data["action"], person_data["facial expression"])
            
            cut_prompt = get_cut_prompt(i, scene_json_data['place'], scene_json_data['time'], scene_json_data['weather'], situations)

            modified_cut_prompt = self.__llm_generator.get_llm(get_image_modify_prompt(), cut_prompt)
            cut_prompts.append(modified_cut_prompt)
        
        return "\n".join(cut_prompts)


''' SYNOPSIS PROMPT '''
SYNOPSIS_PROMPT: str = ""
SYNOPSIS_PROMPT_FILE_PATH = './prompt/synopsis_prompt.txt'

with open(SYNOPSIS_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    SYNOPSIS_PROMPT = f.read()

def get_synopsis_prompt():
    return SYNOPSIS_PROMPT


''' CUT PROMPT '''
CUT_PROMPT: str = ""
CUT_PROMPT_FILE_PATH = "./prompt/cut_prompt.txt"

with open(CUT_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    CUT_PROMPT = f.read()

def get_cut_prompt(i: int, background: str, timeline: str, weather: str, situation: str):
    now_cut_prompt = str(CUT_PROMPT) # str copy

    # 컷의 내용을 기존 형식에 주입시킵니다.
    now_cut_prompt = now_cut_prompt.replace("$i", str(i + 1))
    now_cut_prompt = now_cut_prompt.replace("$background", background)
    now_cut_prompt = now_cut_prompt.replace("$timeline", timeline)
    now_cut_prompt = now_cut_prompt.replace("$weather", weather)

    now_cut_prompt = now_cut_prompt.replace("$situation", situation)

    return now_cut_prompt

''' IMAGE MODIFY PROMPT '''
IMAGE_MODIFY_PROMPT: str = ""
IMAGE_MODIFY_PROMPT_FILE_PATH = './prompt/image_modify_prompt.txt'

with open(IMAGE_MODIFY_PROMPT_FILE_PATH, mode="rt", encoding='utf-8') as f:
    IMAGE_MODIFY_PROMPT = f.read()

def get_image_modify_prompt():
    return IMAGE_MODIFY_PROMPT