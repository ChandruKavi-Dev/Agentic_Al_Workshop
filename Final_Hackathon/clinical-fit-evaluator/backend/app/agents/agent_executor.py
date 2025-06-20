# app/agents/agent_executor.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
# Remove this line if you're not explicitly using BaseModel/Field here for other purposes
# from langchain_core.pydantic_v1 import BaseModel, Field 

# Import the actual tool objects (which are the decorated functions)
from app.agents.tools import (
    analyze_candidate_tool,  # <--- Changed
    extract_culture_tool,    # <--- Changed
    match_traits_tool,       # <--- Changed
    detect_conflicts_tool,   # <--- Changed
    generate_fit_index_tool, # <--- Changed
)

# Gemini LLM as the agent controller
llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-flash", 
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0.3
)

# Register all LangChain-compatible tools
tools = [
    analyze_candidate_tool,
    extract_culture_tool,
    match_traits_tool,
    detect_conflicts_tool,
    generate_fit_index_tool,
]

# Initialize the AgentExecutor using Gemini
clinical_fit_agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True, # Set to True to see the agent's reasoning in your logs
    handle_parsing_errors=True,
    max_iterations=10 # Add a limit to prevent infinite loops
)