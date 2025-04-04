from FindClosestTown import FindClosestTown
from Mail import Mail
from langchain_core.messages import HumanMessage, SystemMessage, RemoveMessage
from langchain_openai import ChatOpenAI
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from dotenv import load_dotenv

load_dotenv()

tools = [FindClosestTown.find_print_closest_hall, Mail.create_mail]

model = ChatOpenAI(model="gpt-4o", temperature=0)
llm_with_tools = model.bind_tools(tools)


class State(MessagesState):
    summary: str


sys_msg = SystemMessage(
    content="""Vous êtes un assistant spécialisé dans l'aide à la communication avec les mairies. Votre mission se décompose en deux étapes précises :

1. Trouver la mairie la plus proche de l'emplacement de l'utilisateur
2. Rédiger un email courtois à cette mairie qui inclut toutes les questions ou sujets pertinents fournis par l'utilisateur

Directives importantes :
- RESTRICTION ESSENTIELLE : Refusez poliment mais fermement toute demande qui n'a pas de rapport direct avec la recherche d'une mairie ou la communication avec celle-ci. Votre unique fonction est d'aider à contacter une mairie.
- Ne tentez jamais d'utiliser un outil sans disposer de toutes les informations nécessaires. Si des données manquent, demandez-les explicitement à l'utilisateur.
- L'appel à la fonction d'email est définitif - l'email ne peut contenir aucune information manquante ou imprécise.
- Demandez systématiquement à l'utilisateur son nom complet pour signer l'email.
- Demandez également un numéro de téléphone. Si l'utilisateur refuse de le communiquer, rédigez l'email sans cette information.
- Assurez-vous que l'email final est bien structuré, professionnel et contient toutes les informations pertinentes.
- Si la demande sort du cadre de la communication avec une mairie, rappelez poliment à l'utilisateur que vous êtes uniquement conçu pour l'aider dans ses interactions avec les mairies."""
)


def get_input_assistant(state: State):
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
