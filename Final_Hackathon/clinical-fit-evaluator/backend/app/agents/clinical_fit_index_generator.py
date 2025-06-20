import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from pydantic import BaseModel, Field

class FitIndex(BaseModel):
    clinical_fit_index: int = Field(description="A single overall score from 0 to 100", ge=0, le=100)
    fit_summary: str = Field(description="A 2-3 sentence summary explaining the score, highlighting strengths and weaknesses.")

def generate_fit_index(trait_matches: list, conflict_risks: list) -> dict:
    parser = JsonOutputParser(pydantic_object=FitIndex)
    llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", google_api_key=os.getenv("GOOGLE_API_KEY"))

    prompt = ChatPromptTemplate.from_messages([
        ("system", "You are a final decision analyst. Given the trait alignment scores and conflict risks, calculate a final 'Clinical Fit Index' score from 0 to 100 and write a concise summary. Your output must be a valid JSON object."),
        ("human", """
            TRAIT MATCHES: {trait_matches}
            CONFLICT RISKS: {conflict_risks}
            
            Based on this data, generate the final score and summary.
            {format_instructions}
        """),
    ])
    
    chain = prompt | llm | parser

    response = chain.invoke({
        "trait_matches": str(trait_matches),
        "conflict_risks": str(conflict_risks),
        "format_instructions": parser.get_format_instructions()
    })
    return response