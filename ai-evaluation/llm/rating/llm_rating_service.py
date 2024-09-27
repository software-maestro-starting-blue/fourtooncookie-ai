from abc import ABCMeta, abstractmethod

class LLMRatingService(ABCMeta):

    '''
    LLM에 대한 점수는 1~5점까지로 주어진다.
    '''
    @abstractmethod
    def get_rating_of_llm(self, user_prompt: str, llm_result: str) -> int:
        pass