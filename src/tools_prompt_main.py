import os

from tool_prompt.utils import PromptToolUtils

from langchain_ollama import ChatOllama

# #################

base_url=os.environ.get('OLLAMA_HOST', 'http://localhost:11434')

# quick warning about meta's llama3.2 failing tool integration out of the box and returns this error -
#
# langchain_core.exceptions.OutputParserException: Could not parse LLM output: `Action: get_now`
# For troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 
# openhermes and mistral both work as is

model = ChatOllama(
    # busted
    # model = "llama3.2:latest",
    # fastest - 
    # model="openhermes",
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