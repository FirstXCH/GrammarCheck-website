from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import asyncio
from googletrans import Translator
import language_tool_python

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

tool = language_tool_python.LanguageTool('en-US')


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("index.html")

@app.post("/check-grammar")
async def check_grammar_and_translate(input_data:TextInput):
    user_text = input_data.text

    translated_text = await get_translation(user_text)

    matches = tool.check(user_text)

    grammar_errors = []
    for m in matches:
        grammar_errors.append({
            "offset": m.offset,
            "error_length": m.error_length,
            "replacements": m.replacements,
            "message": m.message
        })
    return {
        "original_text": user_text,
        "translated_text": translated_text,
        "grammar_errors": grammar_errors
    }

