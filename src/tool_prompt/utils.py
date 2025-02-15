from datetime import datetime
from prompt.date_prompt import DatePrompt

from langchain_core.tools import tool
from langchain_core.prompts import PromptTemplate
from langchain.agents import create_react_agent
from langgraph.prebuilt import ToolExecutor, ToolInvocation, ToolNode


class PromptTools:

    def __init__(self,
                 today=None,
                 origin="US",
                 message_date_format = "MM/DD/YYYY hh:mm:ss p zzz",
                 prompt_tempate_filename=None, 
                 cal_json_filename=None):
        self.date_prompt = DatePrompt(today=today,
                                   origin=origin, 
                                   message_date_format=message_date_format,
                                   prompt_tempate_filename=prompt_tempate_filename,
                                   cal_json_filename=cal_json_filename)

        self.template_text = self.date_prompt.build()
        self.prompt_template = PromptTemplate(template=self.template_text)

        print(f"prompt tools")
        self.tools = self.buildTools()
        self.tool_node = ToolNode(self.tools)

    def buildTools(self):
        return [self.get_now]

    def create_react_agent(self, model):
        return create_react_agent(model, self.tools, self.prompt_template)

    @tool
    def get_now(format: str = "%Y-%m-%d %H:%M:%S"):
        """
        Get the current time
        """
        return datetime.now().strftime(format)
