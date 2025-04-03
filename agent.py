from FindClosestTown import FindClosestTown
from langchain_core.messages import HumanMessage, SystemMessage, RemoveMessage
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

tools = [FindClosestTown.find_print_closest_hall]

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = model.bind_tools(tools)

class State(MessagesState):
    summary: str


sys_msg = SystemMessage(content="You are a helpful assistant tasked with finding the closest town hall to someones location.")

def get_input_assistant(state : State):

    # Get summary if it exists
    summary = state.get("summary", "")

    if summary:
        
        # Add summary to system message
        system_message = f"Summary of conversation earlier: {summary}"

        # Append summary to any newer messages
        messages = [SystemMessage(content=system_message)] + state["messages"]
    
    else:
        messages = state["messages"]

    return {"messages": [llm_with_tools.invoke([sys_msg] + state["messages"])]}

builder = StateGraph(MessagesState)
builder.add_node("assistant", get_input_assistant)
builder.add_node("tools", ToolNode(tools))
builder.add_edge(START, "assistant")
builder.add_conditional_edges(
    "assistant",
    # If the latest message (result) from assistant is a tool call -> tools_condition routes to tools
    # If the latest message (result) from assistant is a not a tool call -> tools_condition routes to END
    tools_condition,
)
builder.add_edge("tools", "assistant")

# Compile graph
graph = builder.compile()