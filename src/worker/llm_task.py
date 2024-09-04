from celery import shared_task
from src.service.zhipu import LLM

@shared_task
def summarize_content(content):
    print("!!!!!!")
    print(content)
    llm = LLM()
    return llm.syncCompletion(content)