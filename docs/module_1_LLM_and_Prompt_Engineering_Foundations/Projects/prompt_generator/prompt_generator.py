from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage 
from langgraph.graph.message import add_messages
from langchain_core.tools import tool 

from langchain_core.messages import SystemMessage, HumanMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import ToolNode 


from langgraph.graph import StateGraph, END 
from langgraph.prebuilt import ToolNode 
from langchain_core.messages import ToolMessage


class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    generated_prompt: str  # store the latest generated prompt
    iteration_count : int # tracks the refinement rounds 

generated_prompt = ""

@tool 
def generate_prompt(optimized_prompt: str) -> str:
    """stores the AI-generated optimized system prompt
    Args:
        optimized_prompt: The fully constructed system prompt
    """
    global generated_prompt
    generated_prompt = optimized_prompt
    return f"Prompt generated successfully!\n\n --- Generated Prompt --- \n {generated_prompt}"

@tool 
def export_prompt(filename: str) -> str:
    """saves the generated prompt to a .txt file
    Args:
        filename: Name for the output file
    """
    global generated_prompt
    if not generated_prompt:
        return "No prompt generated yet. please generate one first."
    
    if not filename.endswith('.txt'):
        filename = f"{filename}.txt"
    
    with open(filename, 'w') as f:
        f.write(generated_prompt)
    
    print(f"\n Prompt saved to : {filename}")
    return f"Promt exported successully to '{filename}'." 


tools = [generate_prompt, export_prompt]

model = ChatOllama(model = "llama3.1:8b").bind_tools(tools, tool_choice = "any")

def prompt_agent(state: AgentState) -> AgentState:
    system_message = SystemMessage(content=f"""
    You are a Prompt Generator assistant.

    When the user gives you a basic request, you MUST follow these steps in order:
    1. Analyze it using the framework below
    2. Construct a detailed, optimized system prompt
    3. CALL THE 'generate_prompt' TOOL IMMEDIATELY with your constructed prompt — do not skip this
    4. Ask if they want refinements or to export it
    5. When user asks to save, CALL THE 'export_prompt' TOOL IMMEDIATELY — do not skip this

    To generate the optimized prompt, transform the user's basic request into a system prompt that includes:

    1. **Role Definition** - Clearly define who/what the AI is
    2. **Core Objective** - State the primary goal explicitly
    3. **Behavioral Rules** - List specific do's and don'ts (at least 5)
    4. **Output Format** - Specify exactly how responses should be structured
    5. **Edge Case Handling** - How to handle ambiguous or off-topic inputs
    6. **Tone & Style** - Communication style guidelines
    7. **Examples** (optional) - 1-2 few-shot examples if beneficial

    Format the optimized prompt as a ready-to-use system prompt, starting with "You are..."

    IMPORTANT TOOL RULES:
    - You MUST call 'generate_prompt' every time you construct or refine a prompt. Never just print it.
    - You MUST call 'export_prompt' when the user asks to save or export. Never skip this step.
    - NEVER write tool calls as text, JSON, or code blocks. You MUST invoke them as actual function calls.  If you describe a tool call instead of making one, that is a failure.

    Current generated prompt:
    {generated_prompt if generated_prompt else "None yet."}
    """)

    print("DEBUG : inside agent node")

    if not state["messages"]:
        # No real user yet — bootstrap with a trigger message
        user_message = HumanMessage(
            content="Hi, I would like a help to generate a prompt."
        )
    else:
        user_input = input("\nYour request or feedback: ")
        print(f"\nUSER: {user_input}")
        user_message = HumanMessage(content = user_input)
    
    print(f"DEBUG : {user_message}")
    
    all_messages = [system_message] + list(state["messages"]) + [user_message]
    response = model.invoke(all_messages)

    # # If the model talked about tools but didn't actually call them, nudge it
    # if not (hasattr(response, "tool_calls") and response.tool_calls):
    #     nudge = HumanMessage(content=(
    #         "You described the tool call but did not actually invoke it. "
    #         "Please call the appropriate tool now — do not write it as text or code."
    #     ))
    #     all_messages_with_nudge = all_messages + [response, nudge]
    #     response = model.invoke(all_messages_with_nudge)

    # print(f"\nAI : \n{response.content}") 
    # if hasattr(response, "tool_calls") and response.tool_calls:
    #     print(f"🔧 TOOLS: {[tc['name'] for tc in response.tool_calls]}")

    if hasattr(response, "tool_calls") and response.tool_calls:
        for tc in response.tool_calls:
            print(f"\n🔧 TOOL CALLED: {tc['name']}")
            # Print the actual prompt being generated, not the raw args
            if tc['name'] == 'generate_prompt':
                print(f"\n📝 GENERATED PROMPT:\n{tc['args'].get('optimized_prompt', '')}")
            elif tc['name'] == 'export_prompt':
                print(f"\n💾 SAVING AS: {tc['args'].get('filename', '')}")
    elif response.content:
        # Only print content if there's no tool call AND content exists
        print(f"\nAI:\n{response.content}")
    
    return {"messages": list(state["messages"]) + [user_message, response]}


def should_continue(state: AgentState) -> str:
    for message in reversed(state["messages"]):
        if (isinstance(message, ToolMessage) and "exported" in message.content.lower()):
            return "end"
    return "continue"

graph = StateGraph(AgentState)
graph.add_node("agent", prompt_agent)
graph.add_node("tools", ToolNode(tools))

graph.set_entry_point("agent")
graph.add_edge("agent", "tools")
graph.add_conditional_edges("tools", should_continue, {
    "continue" : "agent", 
    "end" : END
})

app = graph.compile()

def run():
    print("\n===== PROMPT GENERATOR =====")
    state = {"messages": [], "generated_prompt": "", "iteration_count": 0}
    for step in app.stream(state, stream_mode="values"):
        pass
    print("\n===== DONE =====")

if __name__ == "__main__":
    run()