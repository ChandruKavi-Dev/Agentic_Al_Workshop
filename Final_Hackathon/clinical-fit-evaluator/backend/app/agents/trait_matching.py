import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import List
# Import the new wrapper class
from app.models.schemas import TraitMatch, TraitMatchesList

def match_traits(candidate_traits: dict, hospital_culture: dict) -> List[dict]:
    # 1. Use the new wrapper class for the parser
    parser = JsonOutputParser(pydantic_object=TraitMatchesList) 
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a trait-matching expert for clinical hiring. Compare the candidate's traits with the hospital's values. For each major trait, provide an alignment score from 0 (total mismatch) to 100 (perfect match) and a brief justification. Your output must be a valid JSON object containing a 'matches' key with a list of objects, conforming to the schema."),
        ("human", """
            CANDIDATE TRAITS: {candidate_traits}
            HOSPITAL CULTURE: {hospital_culture}
            
            Please perform the trait matching.
            {format_instructions}
        """),
    ])
    
    chain = prompt | llm | parser
    
    response = chain.invoke({
        "candidate_traits": str(candidate_traits),
        "hospital_culture": str(hospital_culture),
        "format_instructions": parser.get_format_instructions()
    })

    # 2. Extract the list from the response object before returning
    return response['matches']