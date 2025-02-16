# date_prompt_main and tools_prompt_main

I know what you are thinking... could this actually be a moderately complicated LLM langgraph demo app?

Yes, yes one of these is.

First, another mostly pointless demo - 

* [date_prompt_main](src/date_prompt_main.py)

This app illustrates the basics of building a templated prompt that contains many, many options.
 
 ---

Which brings us to the moderately complicated demo - 

* [tools_prompt_main.py](src/tools_prompt_main.py)
    
This small demo flushes out the basic idea of configuring in an <a href="https://ollama.com/">Ollama</a> provided LLM and how to add 'tool' support with a templated prompt.  This app shows the bones of how to create a chat app using LangGraph and runnable agents.  

If new to LangChain or are just confused on the difference of their two apis - think of LangChain as a basic library for interacting with LLMs as 'agents', with LangGraph providing an API acting as an orchestration framework in which you arrange those runnable agents.

--- 

That was a lot of buzzwords... but here goes -

### Prompt templates

    Per langchain docs - a <a href="https://python.langchain.com/docs/concepts/prompt_templates/">Prompt Template</a> offers a template mechanism to translate user input and paramaters into instructions for a language model using plain old english.  
    
    The instructions and parameters in the template can specifiy all sorts of info like output formats, date formats, format in general and so on. The options available are very......varied. 
    
    Check out this [how-to](https://python.langchain.com/docs/how_to/#prompt-templates) guide provided by langchain. It offers a good number of template suggestions, ideas to get you started writing your prompt template for an agent.

### tool nodes

    Langchain "<a href="https://langchain-ai.github.io/langgraph/how-tos/tool-calling/">Tool Calling</a>" enables a "ReAct" agent (could they have choosen a different name for the love of.....moving on) to call functions or as they term it "tools" which provide additional state, information to the agent's LLM.  
    
    The examples of a 'tool' sourced from the link above is get_weather() and get_coolest_cities().  These illustrate the basic idea of what a tool could provide  contextual, and perhaps timely data that was not made part of the LLM when it was trained. 

    Another example of a tool might be something like get_today(). A LLM obviously will not 'know' what day it is unless it is told. Other tools can enable the LLM to do math, gather live statistics, perhaps business/sales data inventory and so on.

### ReAct Agents

    At the heart of a LangGraph app is the idea of an agent. An agent is a runnable piece of code that both accepts and establishes a notion of 'State'. Agents are arranged or orchestrated in a graph, which can have cycles... so enjoy.

Interesting thing to note: Agents don't have to interact with LLMs of course. An agent simply needs to implement well, a Runnable.  Why would you be using LangGraph if you are not interacting with one or more LLMs? Why wouldn't they just be tools available to an LLM to gather data/outputs? I have no idea.  But, hey - you can.



