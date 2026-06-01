import sys
sys.stdout.reconfigure(encoding='utf-8')

import asyncio
from googletrans import Translator
import language_tool_python

text_add = "I swimming in a pool"

# -----------------------------------------
# 1. สร้างฟังก์ชันสำหรับการแปลภาษา (ใช้ async ตามเวอร์ชันของคุณ)
# -----------------------------------------
async def get_translation(text):
    async with Translator() as translator:
        # ต้องมีคำว่า await เพื่อรอให้มันแปลเสร็จก่อน
        result = await translator.translate(text, dest='th')
        return result.text

# รันฟังก์ชันแปลภาษา
translated_text = asyncio.run(get_translation(text_add))

print(f"\nประโยคต้นฉบับ: {text_add}")
print(f"คำแปล: {translated_text}")
print("-" * 30)

# -----------------------------------------
# 2. ส่วนตรวจ Grammar (ทำงานแบบปกติ)
# -----------------------------------------
tool = language_tool_python.LanguageTool('en-US')
matches = tool.check(text_add)

for m in matches:
    print(f"ตำแหน่งที่ผิด (offset): {m.offset} ถึง (error_length): {m.error_length}")
    print(f"คำที่แนะนำ (replacements): {m.replacements}")
    print(f"เหตุผล (message): {m.message}")
    print("-" * 30)

