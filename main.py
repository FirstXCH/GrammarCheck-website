from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.environ.get("GEMINI_API_KEY", ""))
model = genai.GenerativeModel(
  model_name="gemini-3.5-flash",
  generation_config={"response_mime_type": "application/json"}
)
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
    คุณคือผู้เชี่ยวชาญด้านภาษาอังกฤษ ตรวจสอบและแปลข้อความต่อไปนี้: "{user_text}"
    
    ให้ตอบกลับเป็น JSON format เท่านั้น โดยมีโครงสร้างดังนี้:
    {{
        "translated_text": "คำแปลภาษาไทยของข้อความข้างต้น",
        "grammar_errors": [
            {{
                "wrong_word": "คำหรือวลีที่ผิด (ยกมาจากประโยคต้นฉบับเป๊ะๆ)",
                "replacements": ["คำที่ถูกต้องแบบที่ 1", "คำที่ถูกต้องแบบที่ 2"],
                "message": "อธิบายเหตุผลสั้นๆ เป็นภาษาไทยว่าทำไมถึงผิด"
            }}
        ]
    }}
    ถ้าไม่มีอะไรผิดแกรมม่าเลย ให้ส่วน grammar_errors เป็น [] ว่างๆ
    """
    
    try:
        ai_response = model.generate_content(prompt)
        result_dict = json.loads(ai_response.text)
        grammar_errors = result_dict.get("grammar_errors", [])
        translated_text = result_dict.get("translated_text", "")
    except Exception as e:
        print(f"Error from Gemini: {e}")
        grammar_errors = []
        translated_text = "เกิดข้อผิดพลาดในการประมวลผลคำแปล"

    return {
        "original_text": user_text,
        "translated_text": translated_text,
        "grammar_errors": grammar_errors
    }

