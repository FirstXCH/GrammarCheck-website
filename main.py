from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

import google.api_core.exceptions

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
import sys
sys.stdout.reconfigure(encoding='utf-8')

app = FastAPI()

class TextInput(BaseModel):
    text: str


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("templates/index.html")

@app.post("/check-grammar")
async def check_grammar_and_translate(input_data:TextInput):
    user_text = input_data.text

    prompt = f"""
Role: English Grammar Expert.
Task: Check the given text for grammar, spelling, and contextual errors. Provide brief explanations in English.
Output: JSON format only.
{{
    "grammar_errors": [
        {{
            "wrong_word": "exact wrong word from text",
            "replacements": ["correction1", "correction2"],
            "message": "brief English explanation"
        }}
    ]
}}
If no errors, return {{"grammar_errors": []}}

Text: "{user_text}"
"""
    
    MODELS_TO_TRY = [
        "gemini-3.5-flash",
        "gemini-2.5-flash",
        "gemini-3.1-flash-lite",
        "gemini-2.5-flash-lite",
        "gemini-3-flash"
    ]

    grammar_errors = []
    
    for model_name in MODELS_TO_TRY:
        try:
            model = genai.GenerativeModel(
                model_name=model_name,
                generation_config={"response_mime_type": "application/json"}
            )
            ai_response = model.generate_content(prompt)
            result_dict = json.loads(ai_response.text)
            grammar_errors = result_dict.get("grammar_errors", [])
            break
        except google.api_core.exceptions.ResourceExhausted:
            print(f"Model {model_name} hit 429 Limit. Falling back...")
            continue
        except Exception as e:
            print(f"Error with model {model_name}: {e}")
            continue

    return {
        "original_text": user_text,
        "grammar_errors": grammar_errors
    }

