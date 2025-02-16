import os

from tool_prompt.utils import PromptToolUtils

from langchain_ollama import ChatOllama

# #################

base_url=os.environ.get('OLLAMA_HOST', 'http://localhost:11434')

model = ChatOllama(
    # busted out of the box - model="llama3.2:latest",
    # fastest - model="openhermes",
    model = "mistral-small:latest",
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