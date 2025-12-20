import pandas as pd
import base64
import io
from dateutil.parser import parse as parse_date
from app.schemas import parse_rules

def validate_csv(csv_base64: str, schema: dict, options):
    # Decode base64 string into bytes
    decoded = base64.b64decode(csv_base64)

    # Read CSV into a DataFrame
    df = pd.read_csv(io.BytesIO(decoded))

    errors = []

    # Optional cleaning
    if options and getattr(options, "trim_whitespace", False):
        df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    if options and getattr(options, "deduplicate", False):
        df = df.drop_duplicates()

    # Validate each schema column
    for col, rule_str in schema.items():
        rules = parse_rules(rule_str)

        # Column missing?
        if col not in df.columns:
            errors.append({"row": 0, "field": col, "error": "missing column"})
            continue

        # Check each row value in this column
        for idx, value in df[col].items():
            # Row number shown to user (header is row 1 in CSV)
            row_num = idx + 2

            # Required check
            if rules.get("required") and (pd.isna(value) or str(value).strip() == ""):
                errors.append({"row": row_num, "field": col, "error": "required"})
                continue

            # If empty and not required, skip other checks
            if pd.isna(value) or str(value).strip() == "":
                continue

            # Integer checks
            if "int" in rules:
                try:
                    iv = int(value)
                    if "min" in rules and iv < int(rules["min"]):
                        errors.append({"row": row_num, "field": col, "error": f"below min {rules['min']}"})
                    if "max" in rules and iv > int(rules["max"]):
                        errors.append({"row": row_num, "field": col, "error": f"above max {rules['max']}"})
                except:
                    errors.append({"row": row_num, "field": col, "error": "invalid int"})

            # Date checks
            if "date" in rules:
                try:
                    parse_date(str(value))
                except:
                    errors.append({"row": row_num, "field": col, "error": "invalid date"})

            # Simple email check (basic but fine for MVP)
            if "email" in rules:
                if "@" not in str(value):
                    errors.append({"row": row_num, "field": col, "error": "invalid email"})

    return {
        "valid": len(errors) == 0,
        "errors": errors,
        "stats": {
            "rows": len(df),
            "errors": len(errors)
        }
    }
