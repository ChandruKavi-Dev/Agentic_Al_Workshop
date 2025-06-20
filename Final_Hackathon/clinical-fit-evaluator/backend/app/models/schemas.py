from pydantic import BaseModel, Field, ConfigDict, GetCoreSchemaHandler
from pydantic.json_schema import JsonSchemaValue
from pydantic_core import CoreSchema, PydanticCustomError, core_schema
from typing import List, Dict, Any, Optional, Annotated

from bson import ObjectId


# Method 1: PyObjectId (REVISED YET AGAIN - MOST DIRECT & ROBUST)
class PyObjectId(ObjectId):
    """
    Custom ObjectId for Pydantic v2 (MongoDB compatibility)
    """

    @classmethod
    def __get_pydantic_core_schema__(
        cls, source_type: Any, handler: GetCoreSchemaHandler
    ) -> CoreSchema:
        # This function handles both validation (parsing input) and serialization (to string)
        def validate_and_serialize_object_id(value: Any, info: core_schema.ValidationInfo) -> ObjectId:
            # Validation logic
            if isinstance(value, ObjectId):
                return value
            if isinstance(value, str):
                if not ObjectId.is_valid(value):
                    raise PydanticCustomError('object_id', 'Invalid ObjectId string')
                return ObjectId(value)
            if isinstance(value, bytes):
                if len(value) == 12:
                    return ObjectId(value)
                raise PydanticCustomError('object_id', 'Invalid ObjectId bytes length')
            raise PydanticCustomError('object_id', 'Invalid ObjectId type')

        # The core schema now directly uses 'plain_validator_function_ser_schema'
        # which accepts an info argument for both validation and serialization.
        # The 'serialization' argument then specifies how to convert the validated ObjectId
        # to a string for JSON output.
        return core_schema.with_info_plain_validator_function(
            validate_and_serialize_object_id,
            serialization=core_schema.to_string_ser_schema(), # Convert to string for JSON
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: CoreSchema, handler: GetCoreSchemaHandler) -> JsonSchemaValue:
        # This defines how PyObjectId appears in the generated OpenAPI/JSON Schema.
        return {"type": "string", "format": "objectid"}


# Method 3: Using Pydantic's BeforeValidator (Recommended simpler alternative)
# This method is often preferred for its simplicity if you only need a string representation
# of ObjectId and don't need to retain it as a bson.ObjectId instance in Python models.
from pydantic import BeforeValidator

def validate_object_id_str(v):
    if isinstance(v, ObjectId):
        return str(v)
    if isinstance(v, str) and ObjectId.is_valid(v):
        return v
    raise ValueError('Invalid ObjectId')

# Type alias for cleaner usage
ObjectIdStr = Annotated[str, BeforeValidator(validate_object_id_str)]


# Your existing schemas
class CandidateTraits(BaseModel):
    empathy: str = Field(description="e.g., 'High', 'Patient-focused comments observed'")
    leadership_style: str = Field(description="e.g., 'Collaborative', 'Takes initiative in posts'")
    communication_skills: str
    teamwork_collaboration: str
    adaptability: str
    problem_solving: str

class HospitalCulture(BaseModel):
    core_values: List[str] = Field(description="List of core values like 'Patient-First', 'Innovation'")
    work_environment: str = Field(description="e.g., 'Hierarchical', 'Fast-paced', 'Collaborative'")
    mission_focus: str

class TraitMatch(BaseModel):
    trait: str
    candidate_trait_summary: str
    hospital_value_summary: str
    alignment_score: int = Field(ge=0, le=100)
    justification: str

class ConflictRisk(BaseModel):
    risk_level: str = Field(description="'Red', 'Yellow', or 'Green'")
    area: str = Field(description="e.g., 'Communication Style', 'Decision Making'")
    description: str
    justification: str

class FitIndex(BaseModel):
    clinical_fit_index: int = Field(description="A single overall score from 0 to 100", ge=0, le=100)
    fit_summary: str = Field(description="A 2-3 sentence summary explaining the score, highlighting strengths and weaknesses.")

# Using the fixed PyObjectId
class EvaluationResult(BaseModel):
    id: Annotated[Optional[PyObjectId], Field(alias="_id")] = None
    candidate_traits: CandidateTraits
    hospital_culture: HospitalCulture
    trait_matches: List[TraitMatch]
    conflict_risks: List[ConflictRisk]
    clinical_fit_index: int = Field(ge=0, le=100)
    fit_summary: str
    candidate_id: Optional[str] = None
    hospital_id: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str} # Good fallback for other ObjectId fields not using PyObjectId
    )

# Keeping the simpler version for comparison/fallback if needed
class EvaluationResultSimple(BaseModel):
    id: Annotated[Optional[ObjectIdStr], Field(alias="_id")] = None
    candidate_traits: CandidateTraits
    hospital_culture: HospitalCulture
    trait_matches: List[TraitMatch]
    conflict_risks: List[ConflictRisk]
    clinical_fit_index: int = Field(ge=0, le=100)
    fit_summary: str
    candidate_id: Optional[str] = None
    hospital_id: Optional[str] = None

    model_config = ConfigDict(
        populate_by_name=True,
        json_encoders={ObjectId: str}
    )

class TraitMatchesList(BaseModel):
    matches: List[TraitMatch] = Field(description="A list of trait matching analysis results")

class ConflictRisksList(BaseModel):
    risks: List[ConflictRisk] = Field(description="A list of potential conflict risks")