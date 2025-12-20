from fastapi import FastAPI, Header, HTTPException
import os
from app.models import ValidateRequest, ValidateResponse
from app.validator import validate_csv

app = FastAPI(title="CSV Validation API")

@app.post("/validate", response_model=ValidateResponse)
def validate(
    req: ValidateRequest,
    x_api_key: str = Header(None, alias="x-api-key")
):
    single_key = os.getenv("API_KEY")
    keys_csv = os.getenv("VALID_KEYS", "")

    valid_keys = set(k.strip() for k in keys_csv.split(",") if k.strip())

    is_valid = (x_api_key in valid_keys) or (single_key and x_api_key == single_key)

    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid or missing API key")

    return validate_csv(req.csv_base64, req.schema, req.options)
