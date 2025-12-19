from fastapi import FastAPI
from app.models import ValidateRequest, ValidateResponse
from app.validator import validate_csv

app = FastAPI(title="CSV Validation API")

@app.post("/validate", response_model=ValidateResponse)
def validate(req: ValidateRequest):
    result = validate_csv(
        req.csv_base64,
        req.schema,
        req.options
    )
    return result
