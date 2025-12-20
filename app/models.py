from pydantic import BaseModel
from typing import Dict, List, Optional

class ValidationOptions(BaseModel):
    deduplicate: bool = False
    trim_whitespace: bool = True

class ValidateRequest(BaseModel):
    csv_base64: str
    schema: Dict[str, str]
    options: Optional[ValidationOptions] = ValidationOptions()

class ValidationError(BaseModel):
    row: int
    field: str
    error: str

class ValidateResponse(BaseModel):
    valid: bool
    errors: List[ValidationError]
    stats: Dict[str, int]
