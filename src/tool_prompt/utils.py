from datetime import datetime
import pytz
from prompt.date_prompt import DatePrompt
from tool_prompt.agents import AgentState

from langchain.agents import create_react_agent
from langchain_core.prompts import PromptTemplate
from langchain_core.tools import tool
from langgraph.graph import END, StateGraph
from langchain_core.messages import BaseMessage, AIMessage
from langchain_core.runnables import Runnable
from langgraph.prebuilt import ToolNode

default_prompt_datetime_format = "MM/DD/YYYY hh:mm:ss p zzz"

class PromptToolUtils:

    def __init__(self,
                 model=None,
                 today=None,
                 origin="US",
                 message_date_format = default_prompt_datetime_format,
                 prompt_tempate_filename=None, 
                 cal_json_filename=None):
        self.date_prompt = DatePrompt(today=today,
                                   origin=origin, 
                                   message_date_format=message_date_format,
                                   prompt_tempate_filename=prompt_tempate_filename,
                                   cal_json_filename=cal_json_filename)
        self.model = model

        self.template_text = self.date_prompt.build()
        self.prompt_template = PromptTemplate(template=self.template_text)
        self.toolnode = None

        print(f"prompt tools")

    def tools(self):
        return [self.get_now]
    
    def tool_node(self):
        if self.toolnode is None:
            self.toolnode = ToolNode(self.tools())
        return self.toolnode

    def create_react_agent(self) -> Runnable:
        return create_react_agent(self.model, self.tools(), self.prompt_template)
    
    @staticmethod
    def run(prompt_tools, input_text = "Whats the current time?"):
        tool_node = prompt_tools.tool_node()
        agent_runnable = prompt_tools.create_react_agent()

        def create_state_graph():
            return StateGraph(AgentState)
        
        def run_agent(state):
            """
            #if you want to better manages intermediate steps
            inputs = state.copy()
            if len(inputs['intermediate_steps']) > 5:
                inputs['intermediate_steps'] = inputs['intermediate_steps'][-5:]
            """
            agent_outcome = agent_runnable.invoke(state)
            return {"agent_outcome": agent_outcome}

        def should_continue(state):
            messages = [state["agent_outcome"]]
            last_message = messages[-1]
            if "Action" not in last_message.log:
                return "end"
            else:
                return "continue"

        def execute_tools(state):
            print("Called `execute_tools`")
            messages = [state["agent_outcome"]]
            last_message = messages[-1]
            tool_name = last_message.tool

            print(f"Calling tool: {tool_name} last_message.tool_input {last_message.tool_input}")
            
            message_with_tool_call = AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": tool_name,
                        "args": {},
                        "id": "tool_call_id_1",
                        "type": "tool_call",
                    }
                ],
            )
            response = tool_node.invoke({'messages': [message_with_tool_call]})
            return {"intermediate_steps": [(state["agent_outcome"], response)]}

        def compile_workflow():
            workflow = create_state_graph()
            workflow.add_node("agent", run_agent)
            workflow.add_node("action", execute_tools)

            workflow.set_entry_point("agent")

            workflow.add_conditional_edges(
                "agent", should_continue, {"continue": "action", "end": END}
            )

            workflow.add_edge("action", "agent")
            return workflow.compile()

        app = compile_workflow()
        
        inputs = {"input": input_text, "chat_history": []}

        results = []
        last_result = None
        for s in app.stream(inputs):
            last_result = list(s.values())[0]
            results.append(last_result)
        print(f"all results found including intermediate steps - {results}")
        if last_result is not None:
            print("some result found")
            agent_outcome = last_result["agent_outcome"]
            if agent_outcome is not None:
                print("agent outcome found")
                return_values = agent_outcome.return_values
                if return_values is not None and return_values["output"] is not None:
                    print(f"\n--------> {return_values['output']}")


    @tool
    def get_now(format: str = "%Y-%m-%d %H:%M:%S", timezone: str = 'America/New_York'):
        """
        Get the current time
        """
        return datetime.now(tz=pytz.timezone(timezone)).strftime(format)
