from llm.generator.llm_generator import LLMGenerator
from portkey_ai import Portkey

class PortkeyLLMGenerator(LLMGenerator):

    __portkey: Portkey

    def __init__(self, portkey: Portkey):
        self.__portkey = portkey

    def get_llm(self, system_prompt: str, user_prompt: str) -> str:
        response = self.__portkey.chat.completions.create(
            model=self.__gpt_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            timeout=20
        )

        return response.choices[0].message.content
    
    def get_llm_with_prompt_template(self, prompt_id: str, variables: dict) -> str:
        response = self.__portkey.chat.completions.create(
            prompt_id=prompt_id,
            variables=variables,
            timeout=20
        )

        return response.choices[0].message.content