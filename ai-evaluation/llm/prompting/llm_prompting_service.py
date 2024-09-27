from abc import ABCMeta, abstractmethod

class LLMPromptingSerivce(ABCMeta):

    @abstractmethod
    def get_llm_result(self, data: str) -> str:
        pass