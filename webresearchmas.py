from tooltracer import trace_tool, writelogs,toolregistry


import re
from crewai import Agent, Crew, LLM, Process, Task
from crewai.tools import tool
from crewai_tools import SerperDevTool

from langchain_groq import ChatGroq

from dotenv import load_dotenv
load_dotenv()

gemini_llm = LLM(model="groq/llama-3.3-70b-versatile")

search_tool = SerperDevTool()

web_researcher = Agent(
    role="Web Research Specialist",
    goal="Find accurate and recent information from the web for a given topic.",
    backstory=(
            "You are skilled at web research and produce clear, relevant findings "
            "backed by trusted sources."
        ),
    llm=gemini_llm,
    tools=[search_tool],
    verbose=False,
)



#task context tools
summarizer = Agent(
    role="Research Summarizer",
    goal="Create a concise, easy-to-read summary from research findings.",
    backstory=(
            "You convert raw research output into a structured and useful summary "
            "for end users."
        ),
    llm=gemini_llm,
    verbose=False,
)


search_task = Task(
    description=(
            "Search the web for the topic: '{topic}'.\n"
            "Use the Serper tool to gather key points, recent updates, and source links.\n"
            "take top 3 urls.\n"
            "Return results as bullet points"
        ),
    expected_output=(
            "A bullet-point research brief containing key findings."
        ),
    agent=web_researcher,
    )
summary_task = Task(
    description=(
            "Based on the research brief from the previous task and the '{topic}', write a clear summary.\n"
            "make it short and around the context driven "
        ),
    expected_output=(
            "A readable summary with a simple overview paragraph, and source list."
        ),
    agent=summarizer,
    )


# from agentdecorator import runagent
# web_researcher.__dict__['execute_task'] = runagent(web_researcher.execute_task)
# summarizer.__dict__['execute_task'] = runagent(summarizer.execute_task)


runcrew=Crew(
        agents=[web_researcher, summarizer],
        tasks=[search_task, summary_task],
        process=Process.sequential,
        verbose=True
        
    )

@trace_tool
def web_mas(inp: str):
    """ this is a web researcher tool"""
    result = runcrew.kickoff(inputs={"topic":inp})
    result=str(result)
    if "<think>" in result:
     result=re.sub(r'<think>.*?</think>', '', result, flags=re.DOTALL)
    return result


if __name__ == "__main__":
    user_topic = "tell me about tajmahal"
    output =web_mas(user_topic)
    print("\n=== FINAL SUMMARY ===\n")
    print(toolregistry)    
    print(output)
    # writelogs(toolregistry,"config")
    
