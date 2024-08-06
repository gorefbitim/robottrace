import os
import openai as ai
from dotenv import load_dotenv
from tenacity import (  # for exponential backoff
    retry,
    stop_after_attempt,
    wait_random_exponential
)


load_dotenv()

ai.api_key = os.getenv('OPENAI_API_KEY')
MODEL_OLD = "gpt-4-0613"
MODEL_LONG_OLD = "gpt-3.5-turbo-16k"
MODEL = "gpt-3.5-turbo-0613"
MODEL_HIGH = "gpt-4o"  # $15.00 / 1M output tokens


@retry(wait=wait_random_exponential(min=1, max=60), stop=stop_after_attempt(6))
def completion_with_backoff(**kwargs):
    return ai.ChatCompletion.create(**kwargs)


def get_models():
    return [model['id'] for model in ai.Model.list()['data']]
