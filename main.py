from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import asyncio
from googletrans import Translator
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


async def get_translation(text):
    async with Translator() as translator:
        # ต้องมีคำว่า await เพื่อรอให้มันแปลเสร็จก่อน
        result = await translator.translate(text, dest='th')
        return result.text



app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("templates/index.html")

@app.post("/check-grammar")
async def check_grammar_and_translate(input_data:TextInput):
    user_text = input_data.text

    translated_text = await get_translation(user_text)

    prompt = f"""
    คุณคือผู้เชี่ยวชาญด้านไวยากรณ์ภาษาอังกฤษ ตรวจสอบข้อความต่อไปนี้ว่ามีจุดผิดแกรมม่า สะกดคำผิด หรือใช้บริบทผิดหรือไม่
    ถ้ามี ให้ตอบกลับเป็น JSON format เท่านั้น โดยมีโครงสร้างดังนี้:
    {{
        "grammar_errors": [
            {{
                "wrong_word": "คำหรือวลีที่ผิด (ยกมาจากประโยคต้นฉบับเป๊ะๆ)",
                "replacements": ["คำที่ถูกต้องแบบที่ 1", "คำที่ถูกต้องแบบที่ 2"],
                "message": "อธิบายเหตุผลสั้นๆ เป็นภาษาไทยว่าทำไมถึงผิด"
            }}
        ]
    }}
    ถ้าไม่มีอะไรผิดเลย ให้ส่งกลับมาแบบนี้: {{"grammar_errors": []}}
    
    ข้อความที่ต้องตรวจสอบ: "{user_text}"
    """
    
    try:
        ai_response = model.generate_content(prompt)
        result_dict = json.loads(ai_response.text)
        grammar_errors = result_dict.get("grammar_errors", [])
    except Exception as e:
        print(f"Error from Gemini: {e}")
        grammar_errors = []

    return {
        "original_text": user_text,
        "translated_text": translated_text,
        "grammar_errors": grammar_errors
    }

