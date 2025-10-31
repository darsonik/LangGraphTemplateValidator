import os
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
load_dotenv()

LANGSMITH_TRACING=os.getenv("LANGSMITH_TRACING")
LANGSMITH_API_KEY=os.getenv("LANGSMITH_API_KEY")

chat_llm = ChatOpenAI(model = "moonshotai/Kimi-K2-Instruct-0905",
                 base_url=os.getenv("LLM_API_BASE_URL"),
                 api_key=os.getenv("LLM_API_KEY"))

# print(chat_llm.invoke("Hello, world!").content)

