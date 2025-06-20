from langchain.tools import tool
from pydantic import BaseModel
from typing import List, Dict

from app.agents.candidate_profile_analyzer import analyze_candidate_profile
from app.agents.hospital_culture_extractor import extract_hospital_culture
from app.agents.trait_matching import match_traits
from app.agents.conflict_risk_detector import detect_conflict_risks
from app.agents.clinical_fit_index_generator import generate_fit_index

from app.utils.logging import log_tool_execution  # Optional logging decorator


# ------------------ Input Schemas ------------------

class AnalyzeCandidateProfileInput(BaseModel):
    bio: str
    public_content: str


class ExtractCultureInput(BaseModel):
    hospital_url: str
    docs_text: str


class MatchTraitsInput(BaseModel):
    candidate_traits: Dict
    hospital_culture: Dict


class DetectConflictsInput(BaseModel):
    candidate_traits: Dict
    hospital_culture: Dict


class GenerateFitIndexInput(BaseModel):
    matches: List[Dict]
    risks: List[Dict]


# ------------------ Tool Definitions ------------------

@tool(args_schema=AnalyzeCandidateProfileInput)
@log_tool_execution("Analyze Candidate Profile")
def analyze_candidate_tool(bio: str, public_content: str) -> Dict:
    """Analyze the candidate's bio and public content to extract key professional traits."""
    return analyze_candidate_profile(bio, public_content)


@tool(args_schema=ExtractCultureInput)
@log_tool_execution("Extract Hospital Culture")
def extract_culture_tool(hospital_url: str, docs_text: str) -> Dict:
    """Extract hospital culture details from a URL and uploaded documents."""
    return extract_hospital_culture(hospital_url, docs_text)


@tool(args_schema=MatchTraitsInput)
@log_tool_execution("Match Traits")
def match_traits_tool(candidate_traits: Dict, hospital_culture: Dict) -> Dict:
    """Match candidate traits against hospital culture and assign alignment scores."""
    return {"matches": match_traits(candidate_traits, hospital_culture)}


@tool(args_schema=DetectConflictsInput)
@log_tool_execution("Detect Conflict Risks")
def detect_conflicts_tool(candidate_traits: Dict, hospital_culture: Dict) -> Dict:
    """Detect soft-skill or cultural mismatches between candidate and hospital."""
    return {"risks": detect_conflict_risks(candidate_traits, hospital_culture)}


@tool(args_schema=GenerateFitIndexInput)
@log_tool_execution("Generate Clinical Fit Index")
def generate_fit_index_tool(matches: List[Dict], risks: List[Dict]) -> Dict:
    """Generate a clinical fit index score and summary."""
    return generate_fit_index(matches, risks)
