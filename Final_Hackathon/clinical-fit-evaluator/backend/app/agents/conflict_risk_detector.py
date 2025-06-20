import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from typing import List
# Import the new wrapper class
from app.models.schemas import ConflictRisk, ConflictRisksList

def detect_conflict_risks(candidate_traits: dict, hospital_culture: dict) -> List[dict]:
    # 1. Use the new wrapper class for the parser
    parser = JsonOutputParser(pydantic_object=ConflictRisksList)
    
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a risk detection specialist in HR. Based on the candidate's traits and the hospital's culture, identify potential 'soft clashes' or misalignments. Flag each risk as 'Red', 'Yellow', or 'Green'. Provide a justification for each. Your output must be a valid JSON object containing a 'risks' key with a list of objects."),
        ("human", """
            CANDIDATE TRAITS: {candidate_traits}
            HOSPITAL CULTURE: {hospital_culture}

            Identify potential conflicts. For example, an 'independent' candidate in a 'hierarchical' hospital.
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
    return response['risks']