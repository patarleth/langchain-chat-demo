import os

from tool_prompt.utils import PromptToolUtils

from langchain_ollama import ChatOllama

# #################
# FIRST!
# A quick warning about meta's llama3.2 - this model fails tool integration out of the box, returning this error -
#
# langchain_core.exceptions.OutputParserException: Could not parse LLM output: `Action: get_now`
# For troubleshooting, visit: https://python.langchain.com/docs/troubleshooting/errors/OUTPUT_PARSING_FAILURE 
# openhermes and mistral both work as is without any kind of adapter
#
# NEXT!
# Note how the base_url value is sourced.
# When running this app from a vscode devcontainer the OLLAMA_HOST env var is sourced from .devcontainer/devcontainer.json 
#
# OLLAMA_HOST=http://host.docker.internal:11434 
# 
# If you attempt to run this file directly, the base url will be pulled from the env, defaulting to localhost:11434

base_url=os.environ.get('OLLAMA_HOST', 'http://localhost:11434')

model = ChatOllama(
    # bustde
    # model = "llama3.2:latest",
    # fastest - 
    # model="openhermes",
    model = "mistral-small:latest",
    temperature=0,
    base_url=base_url,
    # other params...
)

# #################
pt_name = "date_prompt_template.txt"
pt_name = "json_output_template.txt"

prompt_tools = PromptToolUtils(model=model, prompt_tempate_filename=pt_name)
tools = prompt_tools.tools()

for tool in tools:
    print(tool)

print(prompt_tools.template_text)

PromptToolUtils.run(prompt_tools, input_text = "what was the most notable event that happened in tiananmen square in 1989?")