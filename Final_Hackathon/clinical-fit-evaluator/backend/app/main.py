# app/main.py
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List

# 1. IMPORT THE NEW AGENT-BASED ORCHESTRATOR
from app.services.orchestration_service import run_evaluation_with_agent
from app.models.schemas import EvaluationResult # Ensure this imports your updated EvaluationResult
from app.utils.text_extractor import extract_text_from_file

app = FastAPI(
    title="Clinical Fit Evaluator API",
    description="An AI-powered system to assess candidate-hospital cultural fit.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/evaluate") # The response_model is now more of a guideline, as the final structure is ensured by the agent
async def evaluate_candidate(
    candidate_bio: str = Form(...),
    linkedin_url: str = Form(...),
    additional_urls: List[str] = Form([]),
    hospital_url: Optional[str] = Form(""),
    hospital_docs: List[UploadFile] = File([])
):
    try:
        all_docs_content = []
        for doc in hospital_docs:
            print(f"Processing uploaded file: {doc.filename}")
            extracted_text = extract_text_from_file(doc)
            if extracted_text:
                all_docs_content.append(extracted_text)
        hospital_doc_content = "\n\n--- Next Document ---\n\n".join(all_docs_content)

        # 2. CALL THE NEW AGENT-BASED FUNCTION
        result = await run_evaluation_with_agent(
            candidate_bio=candidate_bio,
            linkedin_url=linkedin_url,
            additional_urls=additional_urls,
            hospital_url=hospital_url,
            hospital_doc_content=hospital_doc_content,
        )
        # Ensure the result is an instance of EvaluationResult or compatible
        # If run_evaluation_with_agent returns a dictionary, convert it
        if isinstance(result, dict):
            # Validate and convert the dict to EvaluationResult for proper Pydantic serialization
            result_model = EvaluationResult(**result)
            return result_model
        return result


    except Exception as e:
        print(f"An error occurred during evaluation in main.py: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"An internal server error occurred: {e}"
        )

@app.get("/")
def read_root():
    return {"message": "Clinical Fit Evaluator API is online and ready."}