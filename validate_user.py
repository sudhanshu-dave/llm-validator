import sys
import json
import os
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

if not os.getenv("OPENAI_API_KEY"):
    print(json.dumps({
        "is_valid": False, 
        "errors": ["Configuration Error: OPENAI_API_KEY not found in .env"], 
        "warnings": []
    }))
    sys.exit(1)

client = OpenAI()

class ValidationResponse(BaseModel):
    is_valid: bool
    errors: List[str]
    warnings: List[str]

def validate_user_profile(user_data: dict) -> ValidationResponse:
    """
    Validates user data using ONLY the LLM, strictly following the assignment rules.
    """
    
    system_prompt = """
    You are a strict data validation assistant. Analyze the input JSON and output a structured response.

    ### PHASE 1: SYNTAX CHECKS (FAILURES = ERRORS)
    *If these fail, add a specific message to 'errors'.*
    
    1. **Name:** Must be present and NOT be empty or whitespace only.
       - Error Message: "Name is required and must be non-empty."
    2. **Phone:** Must start with '+' followed by 10-15 digits.
       - Error Message: "Phone must be in E.164 format (e.g. +1234567890)."
       - CRITICAL: Do NOT check the country code consistency here. Only check the format.
    3. **Country:** Must be a 2-letter uppercase ISO code (e.g. "IN", "US").
       - Error Message: "Country must be a valid 2-letter ISO code."
    4. **Age:** Must be strictly positive (> 0).
       - Error Message: "Age must be a positive number."
    5. **Email:** Must be a valid email format.
       - Error Message: "Invalid email format."

    ### PHASE 2: LOGIC CHECKS (FAILURES = WARNINGS)
    *If these fail, add a specific message to 'warnings'. Do NOT add to 'errors'.*
    
    1. **Phone/Country Mismatch:** Check if the phone prefix matches the Country field.
       - Rule: If Country="IN", phone must start with "+91". If Country="US", phone must start with "+1".
       - Warning Message: "Phone country code does not match the country field."
    2. **Age Logic:** Check if the user is a minor.
       - Rule: If Age is STRICTLY LESS than 18 (e.g., 17, 10), add a warning.
       - Rule: If Age is 18 or older, DO NOT warn.
       - Warning Message: "User is under 18."
    3. **Name Quality:** Check length.
       - Rule: If Name is < 3 chars but not empty.
       - Warning Message: "Name is too short."
    4. **Email Quality:** Check for disposable domains.
       - Warning Message: "Email uses a disposable domain."

    ### PHASE 3: FINAL VERDICT
    - "is_valid": true IF AND ONLY IF 'errors' is empty (even if there are warnings).
    - "is_valid": false IF 'errors' has any items.
    """

    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-mini", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": json.dumps(user_data)}
            ],
            response_format=ValidationResponse,
        )
        return completion.choices[0].message.parsed
        
    except Exception as e:
        return ValidationResponse(
            is_valid=False, 
            errors=[f"System Error: Failed to validate input. {str(e)}"], 
            warnings=[]
        )
    
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({
            "is_valid": False, 
            "errors": ["Usage Error: No input file provided"], 
            "warnings": []
        }))
        sys.exit(1)

    input_file = sys.argv[1]

    try:
        with open(input_file, 'r') as f:
            data = json.load(f)

        result = validate_user_profile(data)
        print(json.dumps(result.model_dump(), indent=2))

    except Exception as e:
        print(json.dumps({"is_valid": False, "errors": [f"File Error: {str(e)}"], "warnings": []}))