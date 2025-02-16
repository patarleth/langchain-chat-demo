import os

from tool_prompt.utils import PromptToolUtils

from langchain_core.prompts import PromptTemplate
from langchain_ollama import ChatOllama

# #################

base_url=os.environ.get('OLLAMA_HOST', 'http://localhost:11434')

model = ChatOllama(
    # model="llama3.3:latest",
    model="openhermes",
    temperature=0,
    base_url=base_url,
    # other params...
)

# #################

prompt_tools = PromptToolUtils(model=model, prompt_tempate_filename="test_template.txt")
tools = prompt_tools.tools()

for tool in tools:
    print(tool)

print(prompt_tools.template_text)

PromptToolUtils.run(prompt_tools)