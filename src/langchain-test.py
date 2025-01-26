from langchain_ollama import ChatOllama
from langchain_core.messages import AIMessage

import os

# https://python.langchain.com/docs/integrations/chat/ollama/

# when running from inside docker -
# In Dockerfile ENV is set with OLLAMA_HOST=http://host.docker.internal:111434 
base_url=os.environ.get('OLLAMA_HOST', 'http://localhost:11434')

llm = ChatOllama(
    model="llama3.2:latest",
    temperature=0,
    base_url=base_url,
    # other params...
)

messages = [
    (
        "system",
        "You are a helpful assistant that translates English to French. Translate the user sentence.",
    ),
    ("human", "Don't borrow precision screwdrivers from Tim. He is a loser and just wants you to drive down and buy him lunch."),
]
ai_msg = llm.invoke(messages)
print(ai_msg.content)