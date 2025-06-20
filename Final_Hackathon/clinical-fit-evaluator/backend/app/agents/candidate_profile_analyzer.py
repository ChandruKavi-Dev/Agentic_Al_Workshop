import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from app.models.schemas import CandidateTraits

def analyze_candidate_profile(bio: str, linkedin_content: str) -> dict:
    """Analyzes candidate data and extracts behavioral traits using Gemini 1.5 Flash."""
    parser = JsonOutputParser(pydantic_object=CandidateTraits)
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are an expert HR analyst specializing in the medical field. Analyze the provided text and extract the candidate's professional traits. Your output must be a valid JSON object that conforms to the provided schema."),
        ("human", """
            Please analyze the following candidate information:
            ---
            CANDIDATE BIO: {bio}
            ---
            LINKEDIN CONTENT / REVIEWS: {linkedin_content}
            ---
            Based on the information, extract the required traits.
            {format_instructions}
        """),
    ])

    chain = prompt | llm | parser
    
    response = chain.invoke({
        "bio": bio,
        "linkedin_content": linkedin_content,
        "format_instructions": parser.get_format_instructions()
    })
    return response