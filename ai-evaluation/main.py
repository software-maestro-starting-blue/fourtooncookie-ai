from openai import OpenAI

from llm.generator.llm_generator import LLMGenerator
from llm.generator.gpt4o_llm_generator import GPT4oLLMGenerator

openai: OpenAI = OpenAI()

llm_service: LLMGenerator = GPT4oLLMGenerator(openai)

def main():
    # data를 가지고 온다.

    # LLMService를 활용한 LLMPromptingService 통해 결과물을 생성한다.
    
    # 생성된 결과물을 LLMRatingService를 활용하여 평가한다.
    pass

if __name__ == '__main__':
    main()