import os
import json
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from app.calendar_tools import check_calendar_availability, create_calendar_booking
from dotenv import load_dotenv

load_dotenv()



def create_agent_executor():
    """Creates the LangChain agent and executor."""
    
    # Get the Google API key from environment variables
    google_api_key = os.getenv("GOOGLE_API_KEY")
    if not google_api_key:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
        

    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0, google_api_key=google_api_key)


    tools = [check_calendar_availability, create_calendar_booking]


    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a helpful assistant named Calendo that helps users book appointments. Today's date is {today}."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])


    agent = create_tool_calling_agent(llm, tools, prompt)

    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    return agent_executor