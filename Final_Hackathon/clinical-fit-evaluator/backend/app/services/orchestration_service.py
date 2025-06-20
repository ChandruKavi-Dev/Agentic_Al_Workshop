# backend/app/services/orchestration_service.py
import os
import json
from datetime import datetime
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from typing import List, Dict, Any, Optional

# Import agent and schemas
from app.agents.agent_executor import clinical_fit_agent
from app.models.schemas import EvaluationResult, PyObjectId

# MongoDB client initialization
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "clinical_fit_db")

try:
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    evaluations_collection = db["evaluations"]
    client.admin.command('ping')
    print("MongoDB connection established successfully.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    raise


async def save_evaluation_result(evaluation_data: Dict[str, Any]) -> EvaluationResult:
    """
    Saves the evaluation result to MongoDB and returns the Pydantic model with the generated _id.
    This function handles the MongoDB insertion logic.
    """
    try:
        if '_id' in evaluation_data and evaluation_data['_id'] is None:
            del evaluation_data['_id']
        if 'id' in evaluation_data and evaluation_data['id'] is None:
            del evaluation_data['id']

        result = evaluations_collection.insert_one(evaluation_data)

        evaluation_data['_id'] = result.inserted_id
        print(f"Evaluation result saved with _id: {result.inserted_id}")

        return EvaluationResult(**evaluation_data)
    except DuplicateKeyError as e:
        print(f"MongoDB Duplicate Key Error: {e}")
        raise
    except Exception as e:
        print(f"An unexpected error occurred during save_evaluation_result: {e}")
        raise


async def run_evaluation_with_agent(
    candidate_bio: str,
    linkedin_url: str,
    additional_urls: List[str],
    hospital_url: str,
    hospital_doc_content: str
) -> Dict[str, Any]:
    """
    Orchestrates the multi-agent workflow for clinical fit evaluation.
    This function prepares the input, runs the agent, validates the output,
    saves it to the database, and returns the final structured result.
    """
    start_time = datetime.now()
    print(f"\n🚀 [{(datetime.now() - start_time).total_seconds():.1f}s] --- Agent-driven Evaluation Started ---")

    public_content = f"LinkedIn Profile: {linkedin_url}"
    if additional_urls:
        valid_urls = [url for url in additional_urls if url]
        if valid_urls:
            public_content += "\nAdditional Links: " + ", ".join(valid_urls)
    
    # --- FIX START ---
    # The agent's input should describe the *goal* and provide *raw data* for its tools to process.
    # It should not contain explicit steps or tool calls.
    # The agent itself decides which tool to use.
    agent_task_description = f"""
    Perform a comprehensive clinical fit evaluation for the candidate doctor with the provided hospital information.
    
    Here is the candidate's data:
    - Candidate Bio: {candidate_bio}
    - Candidate Public Content (LinkedIn, other URLs): {public_content}
    
    Here is the hospital's data:
    - Hospital Website URL: {hospital_url}
    - Hospital Document Content: {hospital_doc_content}
    
    Your process should be:
    1. Analyze the candidate's profile to extract their professional traits.
    2. Extract the hospital's culture details from its website and provided document.
    3. Compare the extracted candidate traits and hospital culture to identify all areas of alignment (trait matches).
    4. Critically identify all potential conflict risks or misalignments between the candidate and the hospital culture. Think broadly about communication styles, work preferences, values, etc., even subtle ones.
    5. Generate a final overall clinical fit index (score 0-100) and a summary based on the trait matches and identified conflict risks.
    6. Your final response MUST be a single JSON object conforming strictly to the EvaluationResult schema. Include all fields: candidate_traits, hospital_culture, trait_matches, conflict_risks, clinical_fit_index, and fit_summary. Do NOT include any other text or formatting.
    """
    
    query_input = {"input": agent_task_description}
    # --- FIX END ---

    print(f"⏳ [{(datetime.now() - start_time).total_seconds():.1f}s] Handing over to Clinical Fit Agent...")

    raw_agent_response = await clinical_fit_agent.ainvoke(query_input)
    
    print(f"✅ [{(datetime.now() - start_time).total_seconds():.1f}s] Agent has finished processing.")
    
    agent_output_content = None
    if isinstance(raw_agent_response, dict) and "output" in raw_agent_response:
        agent_output_content = raw_agent_response["output"]
    elif isinstance(raw_agent_response, str):
        agent_output_content = raw_agent_response
    else:
        print(f"Error: Unexpected raw agent response type: {type(raw_agent_response)}. Raw: {raw_agent_response}")
        raise TypeError("Unexpected agent response format. Expected dict with 'output' or a string.")

    final_result_dict = {}
    if isinstance(agent_output_content, dict):
        final_result_dict = agent_output_content
    elif isinstance(agent_output_content, (str, bytes, bytearray)):
        try:
            final_result_dict = json.loads(agent_output_content)
        except json.JSONDecodeError as e:
            print(f"JSON Parsing Error: Agent output is not valid JSON. Error: {e}")
            print(f"Raw Agent Output Content that failed to parse:\n{agent_output_content}")
            raise ValueError(f"Agent output is not valid JSON: {e}")
    else:
        print(f"Error: Final agent output content is neither a dict nor a parseable string. Type: {type(agent_output_content)}. Content: {agent_output_content}")
        raise ValueError(f"Final agent output content is in an unhandled format.")

    try:
        validated_result_model = EvaluationResult(**final_result_dict)
    except Exception as e:
        print(f"Error validating agent output against EvaluationResult schema: {e}")
        print(f"Malformed dict for debug: {final_result_dict}")
        raise ValueError(f"Agent output did not match expected schema: {e}")

    data_to_save_in_db = validated_result_model.model_dump(by_alias=True, exclude_none=True)

    print(f"⏳ [{(datetime.now() - start_time).total_seconds():.1f}s] Saving to database...")
    saved_evaluation_model = await save_evaluation_result(data_to_save_in_db)

    print(f"✅ [{(datetime.now() - start_time).total_seconds():.1f}s] --- Evaluation Finished ---")
    
    return json.loads(saved_evaluation_model.model_dump_json(by_alias=True))