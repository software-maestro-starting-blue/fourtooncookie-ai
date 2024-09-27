from llm.generator.llm_generator import LLMGenerator
from openai import OpenAI

class GPT4oLLMGenerator(LLMGenerator):

    __open_ai: OpenAI
    __gpt_model: str

    def __init__(self, openai: OpenAI, gpt_model: str = 'gpt-4o'):
        self.__open_ai = openai
        self.__gpt_model = gpt_model

    def get_llm(self, system_prompt: str, user_prompt: str) -> str:
        response = self.__open_ai.chat.completions.create(
            model=self.__gpt_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=20
        )

        return response.choices[0].message.content