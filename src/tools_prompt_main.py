from tool_prompt.utils import PromptTools

from langchain_core.prompts import PromptTemplate

prompt_tools = PromptTools()
tools = prompt_tools.tools

for tool in tools:
    print(tool)

print(prompt_tools.template_text)
