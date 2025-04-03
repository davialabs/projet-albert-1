from FindClosestTown import FindClosestTown
from Mail import Mail
from langchain_core.messages import HumanMessage, SystemMessage, RemoveMessage
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode

tools = [FindClosestTown.find_print_closest_hall, Mail.create_mail]

from langchain_openai import ChatOpenAI
model = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = model.bind_tools(tools)

class State(MessagesState):
    summary: str


sys_msg = SystemMessage(content="""Vous êtes un assistant dont la mission est de trouver la mairie la plus proche de l'emplacement d'une personne et de rédiger un email courtois à cette mairie.

Votre travail se déroule en deux phases :
1. Identifier la mairie la plus proche de l'utilisateur
2. Rédiger un email professionnel qui inclut toutes les questions ou sujets fournis par l'utilisateur

Directives importantes :
- Avant d'utiliser un outil, vérifiez que vous disposez de toutes les informations nécessaires. Si des informations manquent, demandez-les poliment à l'utilisateur.
- L'appel à la fonction d'envoi d'email est définitif. L'email ne peut pas contenir d'informations manquantes.
- Demandez systématiquement à l'utilisateur son nom complet pour signer l'email.
- Demandez également un numéro de téléphone. Si l'utilisateur refuse de le communiquer, rédigez l'email sans cette information.
- Gardez un ton professionnel mais cordial dans toutes vos interactions.
- Assurez-vous que l'email final est bien structuré, sans fautes, et contient toutes les informations pertinentes fournies par l'utilisateur.""")

def get_input_assistant(state : State):

    # Get summary if it exists
    summary = state.get("summary", "")

    if summary:
        
        # Add summary to system message
        system_message = f"Résumé de la conversation précédente: {summary}"

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