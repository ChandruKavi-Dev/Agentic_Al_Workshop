# agents.py
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.schema.runnable import RunnablePassthrough
from langchain.schema.output_parser import StrOutputParser

from rag_pipeline import get_retriever

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.7)

# 1. Career History Parser Agent
def get_parser_agent():
    """
    This agent extracts and structures user's career history from free-form text.
    """
    prompt_template = """
    You are an expert HR analyst. Your task is to parse the following user input and extract key information into a structured summary.
    Identify and list the following:
    - Academic Background (University, Degree, Graduation Year)
    - Current Role (Job Title, Organization, Years of Experience)
    - Stated Interests (Keywords or phrases mentioned by the user about their career goals)
    - Key Skills (Technical or soft skills mentioned)

    User Input:
    "{user_input}"

    Structured Summary:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["user_input"])
    return LLMChain(prompt=prompt, llm=llm)

# 2. Path Recommender Agent (RAG-Enabled)
def get_recommender_agent():
    """
    This RAG-enabled agent recommends career paths by combining user history with retrieved documents.
    """
    retriever = get_retriever()

    prompt_template = """
    You are an AI medical career mentor. Your goal is to recommend 3-5 potential career paths for a junior healthcare professional based on their background and interests.
    Use the provided context from career documents to make your recommendations relevant and evidence-based. For each path, provide a brief description and why it's a good fit.

    CONTEXT from career documents:
    {context}

    USER'S CAREER SUMMARY:
    {user_summary}

    Recommended Career Paths:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["context", "user_summary"])

    # Create the RAG chain
    rag_chain = (
        {"context": retriever, "user_summary": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return rag_chain

# 3. Mentor & Resource Matcher Agent
def get_matcher_agent():
    """
    This agent suggests mentors and resources based on the recommended career paths.
    """
    prompt_template = """
    You are a resource coordinator for healthcare professionals. Based on the following recommended career paths, suggest specific resources to help the user explore them.
    For each path, suggest:
    1. A type of mentor they should look for (e.g., 'A senior cardiologist with research experience').
    2. A relevant professional organization or society.
    3. A key journal or publication to follow.

    Recommended Career Paths:
    "{recommended_paths}"

    Mentors and Resources:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["recommended_paths"])
    return LLMChain(prompt=prompt, llm=llm)

# 4. Career Path Visualizer Agent
def get_visualizer_agent():
    """
    This agent generates a structured representation of career paths suitable for visualization.
    It outputs in a simplified DOT-like format.
    """
    prompt_template = """
    You are an AI that structures career data for visualization. Convert the following recommended career paths into a simple, hierarchical list.
    For each main path, list 2-3 key milestones or choices as sub-items.

    Example Input:
    "Path 1: Clinical Research. This involves..."
    "Path 2: Healthcare Administration. This requires an MHA..."

    Example Output:
    "Career Start" -> "Clinical Research"
    "Clinical Research" -> "Complete GCP Certification"
    "Clinical Research" -> "Join a Clinical Research Organization (CRO)"
    "Career Start" -> "Healthcare Administration"
    "Healthcare Administration" -> "Pursue an MHA/MBA"
    "Healthcare Administration" -> "Seek a role in hospital operations"

    Now, process the following input:
    Recommended Career Paths:
    "{recommended_paths}"

    Visualization Data:
    """
    prompt = PromptTemplate(template=prompt_template, input_variables=["recommended_paths"])
    return LLMChain(prompt=prompt, llm=llm)