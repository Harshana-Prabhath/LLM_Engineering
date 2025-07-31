from dotenv import load_dotenv
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from browsers import create_async_playwright_browser,create_sync_playwright_browser
import sys
import asyncio
import nest_asyncio
import textwrap
from send_email import send_email
from langchain_openai import ChatOpenAI
from langgraph.graph import StateGraph, START, END
from State import State
from langgraph.prebuilt import ToolNode, tools_condition
import gradio as gr
from langgraph.checkpoint.memory import InMemorySaver
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from State import NavigationType, ExtractType
from langchain_tavily import TavilySearch

nest_asyncio.apply()

async def main ():

    load_dotenv(override=True)

    

    tavily_seaerch_tool = TavilySearch(
         max_results=5,
        topic="general",
    )
    
    
    

    tools = [tavily_seaerch_tool,send_email]

    print(tools)

    llm = ChatOpenAI()

    graph_builder = StateGraph(State)

    llm_with_tool = llm.bind_tools(tools)


    def chatbot(state:State):
        
        return {"messages": [llm_with_tool.invoke(state["messages"])]}
    
    graph_builder.add_node("chatbot",chatbot)

    graph_builder.add_node("tools",ToolNode(tools=tools))

    graph_builder.add_conditional_edges(
        "chatbot",
        tools_condition,
        {"tools":"tools",END:END}

    )
    graph_builder.add_edge("tools","chatbot")

    graph_builder.add_edge(START,"chatbot")

    memory = InMemorySaver()

    graph = graph_builder.compile(checkpointer=memory)

    config = {"configurable":{"thread_id":"1"}}


    def chat(user_input:str,history):
        first_state = State(messages=[
            {"role":"user","content":user_input},
            {"role": "system", "content": "You are a smart agent with access to tools like 'navigate_browser' and 'extract_text'. Use them when needed."},
            ])
        result = graph.invoke(first_state, config=config)
        return result["messages"][-1].content
    

    gr.ChatInterface(fn=chat, type="messages").launch()





    

asyncio.run(main())