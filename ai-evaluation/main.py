from openai import OpenAI

from llm.generator.llm_generator import LLMGenerator
from llm.generator.gpt4o_llm_generator import GPT4oLLMGenerator
from llm.prompting.llm_prompting_service import LLMPromptingSerivce
from llm.rating.llm_rating_service import LLMRatingService

import json

openai: OpenAI = OpenAI()

llm_service: LLMGenerator = GPT4oLLMGenerator(openai)

llm_prompting_service: LLMPromptingSerivce = None # 테스트를 진행할 prompting service

llm_rating_services: list[LLMRatingService] = []

def main():
    # data를 가지고 온다.
    f = open("input_data.json", "r")
    input_datas = json.load(f)
    f.close()

    # LLMService를 활용한 LLMPromptingService 통해 결과물을 생성한다.
    data_sets = [
        (input_data, llm_prompting_service.get_llm_result(input_data))
        for input_data in input_datas
    ]
    
    # 생성된 결과물을 LLMRatingService를 활용하여 평가한다.
    rating_results = [
        [
            llm_rating_service.get_rating_of_llm(user_input, llm_result)
            for llm_rating_service in llm_rating_services
        ]
        for user_input, llm_result in data_sets
    ]
    
    # data_sets와 rating_results를 합쳐서 결과를 만든다.
    results = [
        {
            "user_input": user_input,
            "llm_result": llm_result,
            "ratings": ratings
        }
        for (user_input, llm_result), ratings in zip(data_sets, rating_results)
    ]
    
    # 각 rating의 평균을 출력한다.
    for i, llm_rating_service in enumerate(llm_rating_services):
        ratings = [result["ratings"][i] for result in results]
        average_rating = sum(ratings) / len(ratings)
        print(f"Average rating of {llm_rating_service.__class__.__name__}: {average_rating}")
    
    # 결과를 json으로 저장한다.
    f = open("rating_result.json", "w")
    json.dump(results, f)
    f.close()

if __name__ == '__main__':
    main()