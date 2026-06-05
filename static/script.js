// Theme Setup
const currentTheme = localStorage.getItem("theme") || "light";
document.documentElement.setAttribute("data-theme", currentTheme);
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("themeIcon").innerText =
    currentTheme === "dark" ? "🌙" : "☀️";
});

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  const newTheme = current === "dark" ? "light" : "dark";
  document.documentElement.setAttribute("data-theme", newTheme);
  localStorage.setItem("theme", newTheme);
  document.getElementById("themeIcon").innerText =
    newTheme === "dark" ? "🌙" : "☀️";
}

let currentErrors = [];

async function checkGrammar() {
  const text = document.getElementById("inputText").value;
  if (!text) {
    alert("กรุณาพิมพ์ข้อความก่อนครับ!");
    return;
  }

  document.getElementById("resultArea").style.display = "block";
  document.getElementById("grammarErrorsList").innerHTML = "<div style='text-align: center; padding: 20px; color: #666;'>กำลังประมวลผล...</div>";
  document.getElementById("acceptAllBtn").style.display = "none";

  try {
    const response = await fetch("/check-grammar", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text: text }),
    });

    const data = await response.json();

    currentErrors = data.grammar_errors || [];
    renderErrors();
    updateHighlights();
  } catch (error) {
    alert("เกิดข้อผิดพลาดในการเชื่อมต่อกับเซิร์ฟเวอร์");
    console.error(error);
  }
}

function renderErrors() {
  const errorList = document.getElementById("grammarErrorsList");
  const acceptAllBtn = document.getElementById("acceptAllBtn");
  errorList.innerHTML = "";

  if (currentErrors.length === 0) {
    errorList.innerHTML = "<div class='success-message'>🎉 ไม่มีข้อผิดพลาด! เก่งมากครับ</div>";
    acceptAllBtn.style.display = "none";
  } else {
    acceptAllBtn.style.display = "block";
    currentErrors.forEach((err, index) => {
      const suggestion =
        err.replacements.length > 0 ? err.replacements[0] : "ไม่มีคำแนะนำ";
      const wrongText = err.wrong_word || "ข้อความที่ผิด";

      const card = document.createElement("div");
      card.classList = "error-card";
      card.innerHTML = `
          <div class="card-header">💡 ${err.message}</div>
          <div class="card-body">
              <span class="wrong-word">${wrongText}</span> 👉 <span class="correct-word">${suggestion}</span>
          </div>
          <button class="accept-btn" onclick="applyFix(${index})">
              ✅ Accept
          </button>
      `;
      errorList.appendChild(card);
    });
  }
}

function applyFix(index) {
  const err = currentErrors[index];
  if (!err) return;

  const suggestion =
    err.replacements.length > 0 ? err.replacements[0] : "ไม่มีคำแนะนำ";
  const wrongText = err.wrong_word || "ข้อความที่ผิด";

  if (suggestion === "ไม่มีคำแนะนำ") return;
  const textArea = document.getElementById("inputText");
  textArea.value = textArea.value.replace(wrongText, suggestion);

  // ลบ error ใบนี้ออก
  currentErrors.splice(index, 1);
  renderErrors();
  handleInput();
}

function acceptAll() {
  const textArea = document.getElementById("inputText");
  let newText = textArea.value;

  currentErrors.forEach((err) => {
    const suggestion = err.replacements.length > 0 ? err.replacements[0] : null;
    if (suggestion && err.wrong_word) {
      newText = newText.replace(err.wrong_word, suggestion);
    }
  });

  textArea.value = newText;
  currentErrors = [];
  renderErrors();
  handleInput();
}

// ---------------- UI Helpers ----------------

function handleInput() {
  const text = document.getElementById("inputText").value;
  const pasteBtn = document.getElementById("pasteBtn");
  const copyBtn = document.getElementById("copyBtn");

  if (text.trim() === "") {
    pasteBtn.style.display = "inline-block";
    copyBtn.style.display = "none";
  } else {
    pasteBtn.style.display = "none";
    copyBtn.style.display = "inline-block";
  }
  updateHighlights();
}

function handleScroll() {
  const textarea = document.getElementById("inputText");
  const backdrop = document.getElementById("backdrop");
  backdrop.scrollTop = textarea.scrollTop;
  backdrop.scrollLeft = textarea.scrollLeft;
}

function updateHighlights() {
  const text = document.getElementById("inputText").value;
  // ป้องกัน XSS
  let escapedText = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  currentErrors.forEach((err) => {
    const wrongText = err.wrong_word;
    if (wrongText && escapedText.includes(wrongText)) {
      escapedText = escapedText.replace(wrongText, `<mark>${wrongText}</mark>`);
    }
  });

  // แสดง newline ให้ถูกต้องใน div
  document.getElementById("backdrop").innerHTML = escapedText + "<br>"; // +br helps scroll match
}

async function copyText() {
  const text = document.getElementById("inputText").value;
  await navigator.clipboard.writeText(text);
  const copyBtn = document.getElementById("copyBtn");
  copyBtn.innerText = "✅ Copied!";
  setTimeout(() => {
    copyBtn.innerText = "📄 Copy";
  }, 2000);
}

async function pasteText() {
  try {
    const text = await navigator.clipboard.readText();
    document.getElementById("inputText").value = text;
    handleInput();
  } catch (err) {
    alert(
      "เบราว์เซอร์ไม่รองรับการวางอัตโนมัติ กรุณากด Ctrl+V หรือ Command+V ครับ",
    );
  }
}
