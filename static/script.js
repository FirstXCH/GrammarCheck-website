async function checkGrammar() {
  const text = document.getElementById("inputText").value;
  if (!text) {
    alert("กรุณาพิมพ์ข้อความก่อนครับ!");
    return;
  }

  // แสดงหน้าโหลด หรือ ล้างข้อมูลเก่า
  document.getElementById("resultArea").style.display = "block";
  document.getElementById("translationResult").innerText = "กำลังประมวลผล...";
  document.getElementById("grammarErrorsList").innerHTML = "";

  try {
    // ส่งข้อมูลไปที่ Backend
    const response = await fetch("/check-grammar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text }),
    });

    const data = await response.json();

    // 1. แสดงคำแปล
    document.getElementById("translationResult").innerText =
      data.translated_text;

    // 2. แสดง Grammar ที่ผิด
    const errorList = document.getElementById("grammarErrorsList");
    errorList.innerHTML = ""; // ล้างของเก่า

    if (data.grammar_errors.length === 0) {
      errorList.innerHTML = "<li>ไม่มีข้อผิดพลาด! เก่งมากครับ 🎉</li>";
    } else {
      data.grammar_errors.forEach((err) => {
        const suggestion =
          err.replacements.length > 0 ? err.replacements[0] : "ไม่มีคำแนะนำ";

        const wrongText = text.substring(
          err.offset,
          err.offset + err.error_length,
        );

        const card = document.createElement("div");
        card.classList = "error-card";

        card.innerHTML = `
            <div class="card-header">💡 ${err.message}</div>
                    <div class="card-body">
                        <!-- คำที่ผิด (ขีดฆ่าสีแดง) -->
                        <span class="wrong-word">${wrongText}</span> 
                        👉 
                        <!-- คำที่ถูก (สีเขียว) -->
                        <span class="correct-word">${suggestion}</span>
                    </div>
                    <button class="accept-btn" onclick="applyFix('${suggestion}')">
                        ✅ Accept
                    </button>
          `;

        errorList.appendChild(card);
      });
    }
  } catch (error) {
    alert("เกิดข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์");
    console.error(error);
  }
}
// ฟังก์ชันสำหรับเวลากดปุ่ม Accept
function applyFix(suggestedWord) {
  if (suggestedWord === "ไม่มีคำแนะนำ") return;

  // (ในอนาคตเราสามารถเขียนโค้ดให้มันไปแทนที่คำผิดในประโยคเดิมได้
  // แต่เบื้องต้น เอาคำที่ถูกไปต่อท้าย หรือแสดงให้ดูก่อนครับ)
  alert(
    "คุณยอมรับคำว่า: " +
      suggestedWord +
      "\n(เดี๋ยวสเต็ปต่อไปเราจะทำให้มันไปแก้ในช่องพิมพ์ให้อัตโนมัตินะครับ!)",
  );
}
