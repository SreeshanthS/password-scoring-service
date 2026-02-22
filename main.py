from fastapi import FastAPI
from pydantic import BaseModel
import re

app = FastAPI(title="Password Strength Scoring Service")

class PasswordRequest(BaseModel):
    password: str

@app.get("/health")
def health():
    return {"status": "Service is running"}

@app.post("/score")
def score_password(request: PasswordRequest):
    password = request.password
    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 20
    else:
        suggestions.append("Use at least 8 characters")

    if re.search(r"[A-Z]", password):
        score += 20
    else:
        suggestions.append("Add uppercase letters")

    if re.search(r"[a-z]", password):
        score += 20
    else:
        suggestions.append("Add lowercase letters")

    if re.search(r"[0-9]", password):
        score += 20
    else:
        suggestions.append("Include numbers")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 20
    else:
        suggestions.append("Add special characters")

    if score <= 40:
        strength = "Weak"
    elif score <= 80:
        strength = "Medium"
    else:
        strength = "Strong"

    return {
        "score": score,
        "strength": strength,
        "suggestions": suggestions
    }