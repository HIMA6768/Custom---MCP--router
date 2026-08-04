from crewai import Agent,Task,Crew,LLM
from crewai.tools import tool
from dotenv import load_dotenv
import json
from importlib import import_module
import sys
from execution import runtool


load_dotenv()

filepath=r"C:\Users\HIMADRI\Desktop\mas evaluation system\environment\config.json"
with open(filepath,"r") as f:
    configurefile=json.load(f)
print(configurefile)

llm= LLM(model="groq/llama-3.3-70b-versatile")


@tool("Tool Execution Engine")
def engine(name: str, input: str) -> str:
    """
    Use this tool to execute any registered MAS or tool. 
    Provide the exact tool name and the input query/argument.
    """
    result = runtool(name, input,configurefile)
    return str(result)



superagent = Agent(
    role="Master Cognitive Orchestrator & Dynamic Router",
    goal="Meticulously analyze user intent, cross-reference with the tool registry using Chain-of-Thought reasoning, and flawlessly dispatch execution.",
    backstory=(
        "You are an elite, highly deterministic meta-agent modeled after advanced cognitive architectures. "
        "You do not guess or hallucinate tool names. You evaluate user queries against available "
        "schemas, deduce the optimal path, and execute actions with absolute precision."
    ),
    llm=llm,
    tools=[engine],  
    verbose=True,
)


superagent_task = Task(
    description=(
        f"### CONTEXT & REGISTRY\n"
        f"Here is the absolute list of available tools/MAS registered in the system:\n"
        f"{configurefile}\n\n"
        
        f"### USER QUERY\n"
        f"'{'{query}'}'\n\n"
        
        f"### EXECUTION PROTOCOL (Chain-of-Thought):\n"
        f"Follow these steps sequentially before calling the tool:\n"
        f"1. **Intent Analysis:** Break down what the user is explicitly trying to achieve.\n"
        f"2. **Registry Mapping:** Scan the provided registry above. Match the intent strictly with a tool's 'name' and its expected functionality/arguments.\n"
        f"3. **Argument Extraction:** Extract the exact parameter value from the user query required by that tool.\n"
        f"4. **Execution:** Invoke the 'Tool Execution Engine' tool with the precise `tool_name` and extracted `user_input`.\n\n"
        
        f"### FEW-SHOT EXAMPLES:\n"
        f"- If query is 'Add 5 and 10' -> Match with addition tool -> Call engine with tool_name='addition_tool' (or respective name) and user_input='5,10' (or as per schema).\n"
        f"- If query is 'What is quantum computing?' -> Match with web researcher -> Call engine with tool_name='web_mas' and user_input='What is quantum computing?'\n\n"
        
        f"### STRICT GUARDRAILS:\n"
        f"- Do NOT invent tool names. Use ONLY exact names from the registry.\n"
        f"- If a query matches no available tools, gracefully explain why instead of crashing."
    ),
    expected_output=(
        "A structured execution trace showing Intent Analysis, Tool Selection, "
        "the final output returned by the Tool Execution Engine."
        "The answer of the query"
    ),
    agent=superagent
)

supercrew=Crew(
    agents=[superagent],
    tasks=[superagent_task],
    varbose=True

)

def superengine(inp: str):
    result = supercrew.kickoff(inputs={"query":inp})
    return str(result)

if __name__=="__main__":
    question= " what is the capital of india"
    output=superengine(question)
    print("_________________FINAL OUTPUT________________________")
    print(output)
