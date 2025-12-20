from fastapi import FastAPI, Header, HTTPException
import os
from app.models import ValidateRequest, ValidateResponse
from app.validator import validate_csv

app = FastAPI(title="CSV Validation API")

@app.post("/validate", response_model=ValidateResponse)
def validate(
    req: ValidateRequest,
    x_api_key: str = Header(None)
):
    expected_key = os.getenv("API_KEY")

    if not expected_key or x_api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    result = validate_csv(
        req.csv_base64,
        req.schema,
        req.options
    )
    return result
