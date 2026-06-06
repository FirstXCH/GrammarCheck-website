# 📝 GrammarCheck-website

เป็นโปรเจกต์แรกที่ผมทำขึ้นมาเพราะ ผมกำลังเรียนภาษาอังกฤษไปด้วยเป็นเว็บพิมพ์ประโยคตรวจสอบแกรมม่าโดย AI และ ผมพึ่งลองเรียนภาษา python แล้วอยากนำ api มาใช้สร้างเว็บด้วย

<div align="center">
  <img width="800" alt="Grammar Check Web Screenshot" src="https://github.com/user-attachments/assets/fcb72789-8287-4714-b52c-af1766ee8ad3" />
</div>

## 🧠 สิ่งที่ได้เรียนรู้จากโปรเจกต์นี้

1.การจัดการไฟล์ให้เป็นระเบียบเราควรแยก หน้าบ้าน-หลังบ้าน จะได้แก้ไขได้ง่ายตอน Error หรือสั่ง AI (ใช้ AI แยกว่าไฟล์เอาไปอยู่ตรงไหนเป็นระเบียบ กับตั้งชื่อไฟล์)

2.การดึง API (fastapi,gemini) ก็ได้ลองเปิด docs ดูบ้างว่ามันทำได้เยอะมากที่ผมทำแค่เบื้องต้นง่ายๆ 

3.เข้าใจ Basic Syntax ภาษา JavaScript จากที่ตาลายอ่านไม่ค่อยรู้เรื่อง แล้วก็ DOM การโต้ตอบหน้าเว็บ-หลังบ้านเพื่อรับหรือส่งแสดงผล (ส่วน HTML , CSS ผมให้ AI เขียนหมดเลย แต่เข้าใจอยู่ว่าบรรทัดนี้กล่าวถึง class ไหนใน CSS)

4.ข้อมูล JSON เข้าใจว่ามันก็คือ key : value กับมีคำสั่งแปลงข้อมูลอีกที

5.ผมควรทำขั้นตอนการทำงานเป็นข้อที่ละเอียดมากขึ้น ผมรู้แค่ว่าใส่ Input แล้วเอาไปเช็ค AI จากนั้นแสดงผลลัพธ์ (ไม่ได้รู้ละเอียดขั้นว่าต้อง fecth, forEach , JSON file ทั้งรับส่ง)

6.การลองอัพขึ้น git and .env (ไว้เก็บข้อมูลสำคัญ) ตอนอัพ git ตอนแรกก็ลองพิมพ์อัพเอง แต่สักพัก AI สะดวกกว่าแต่ปัญหาคือมันชอบอัพขึ้นตอนให้แก้นิดเดียวผมยังไม่ accept จริงๆมันตั้งได้แต่ผมให้มัน auto อิอิ😆

## 🚀 Tech Stack

* **Frontend:** HTML, CSS, Vanilla JavaScript
* **Backend:** Python, FastAPI
* **AI Integration:** Google Generative AI (Gemini API)

## ✨ Features
- 📝 ตรวจสอบไวยากรณ์ภาษาอังกฤษและแนะนำการแก้ไขพร้อมคำอธิบาย
- 📋 มีปุ่ม Copy/Paste ข้อความด่วน
- 🌗 Dark Mode / Light Mode
- ⚡ AI free model วิเคราห์ะผลลัพย์อาจไม่ถูกต้องหรือ limit

## 🛠️ วิธีติดตั้งและรันโปรเจกต์ (Local Setup)

1. Clone โปรเจกต์นี้ลงเครื่อง
```bash
git clone https://github.com/FirstXCH/GrammarCheck-website.git
```
2.ติดตั้งไลบรารี
```bash
pip install -r requirements.txt
```
3.สร้างไฟล์ .env ในโฟลเดอร์เดียวกับ main.py และใส่ API Key ของ Gemini

GEMINI_API_KEY = ใส่_API_KEY_

4.รันเซิร์ฟเวอร์
```bash
uvicorn main:app --reload
```
5.เปิดเบราว์เซอร์ http://127.0.0.1:8000


