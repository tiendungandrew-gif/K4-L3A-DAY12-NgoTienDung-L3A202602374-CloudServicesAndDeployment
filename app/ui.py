"""Trang giao diện Web Chatbot AI cho Day 12 Agent.

Bao gồm hoạt họa SVG 2D Chú vịt đạp xe (Cycling Duck) độc quyền,
kết nối trực tiếp tới endpoint /ask, /health, /ready.
"""

def get_chat_ui_html() -> str:
    return """<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>QuackBot — Cloud AI Agent (Day 12)</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
  <style>
    :root {
      --bg-gradient: radial-gradient(circle at 50% 0%, #1a1f35 0%, #0b0f19 100%);
      --surface: rgba(18, 24, 38, 0.75);
      --surface-border: rgba(255, 255, 255, 0.08);
      --primary: #38bdf8;
      --primary-hover: #0284c7;
      --accent: #facc15;
      --accent-orange: #fb923c;
      --text: #f1f5f9;
      --text-muted: #94a3b8;
      --card-user: linear-gradient(135deg, #3b82f6 0%, #6366f1 100%);
      --card-bot: rgba(30, 41, 59, 0.65);
      --radius: 18px;
    }

    * {
      box-sizing: border-box;
      margin: 0;
      padding: 0;
      font-family: 'Outfit', sans-serif;
    }

    body {
      background: var(--bg-gradient);
      color: var(--text);
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: space-between;
      overflow-x: hidden;
      padding: 16px;
    }

    /* Track bar for cycling duck */
    .duck-track {
      width: 100%;
      max-width: 900px;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid var(--surface-border);
      border-radius: 24px;
      padding: 8px 16px;
      margin-bottom: 12px;
      position: relative;
      overflow: hidden;
      height: 90px;
      display: flex;
      align-items: center;
      backdrop-filter: blur(12px);
    }

    .road-line {
      position: absolute;
      bottom: 14px;
      left: 0;
      right: 0;
      height: 2px;
      background: repeating-linear-gradient(90deg, #38bdf8 0, #38bdf8 15px, transparent 15px, transparent 30px);
      animation: roadMove 1.5s linear infinite;
      opacity: 0.4;
    }

    @keyframes roadMove {
      from { transform: translateX(0); }
      to { transform: translateX(-30px); }
    }

    .cycling-duck-container {
      position: absolute;
      bottom: 12px;
      left: 20px;
      display: flex;
      align-items: center;
      gap: 12px;
      transition: left 0.4s ease;
    }

    .duck-speech {
      background: rgba(250, 204, 21, 0.15);
      border: 1px solid rgba(250, 204, 21, 0.4);
      color: #fef08a;
      padding: 6px 14px;
      border-radius: 12px;
      font-size: 13px;
      font-weight: 500;
      white-space: nowrap;
      position: relative;
      box-shadow: 0 4px 15px rgba(250, 204, 21, 0.1);
      animation: float 2.5s ease-in-out infinite;
    }

    @keyframes float {
      0%, 100% { transform: translateY(0); }
      50% { transform: translateY(-4px); }
    }

    /* SVG Duck & Bike Animations */
    .wheel {
      transform-origin: center;
      animation: spin 1s linear infinite;
    }
    .wheel.fast {
      animation-duration: 0.3s !important;
    }
    @keyframes spin {
      100% { transform: rotate(360deg); }
    }

    .duck-leg {
      transform-origin: 35px 45px;
      animation: pedal 1s linear infinite;
    }
    .duck-leg-2 {
      transform-origin: 35px 45px;
      animation: pedal 1s linear infinite -0.5s;
    }
    @keyframes pedal {
      0% { transform: rotate(0deg); }
      50% { transform: rotate(180deg); }
      100% { transform: rotate(360deg); }
    }

    .duck-body-group {
      animation: bounce 0.5s ease-in-out infinite alternate;
    }
    @keyframes bounce {
      from { transform: translateY(0); }
      to { transform: translateY(-2px); }
    }

    /* Main Container */
    .app-container {
      width: 100%;
      max-width: 900px;
      height: calc(100vh - 140px);
      background: var(--surface);
      backdrop-filter: blur(20px);
      border: 1px solid var(--surface-border);
      border-radius: 28px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5), 0 0 60px rgba(56, 189, 248, 0.05);
      overflow: hidden;
    }

    /* Header */
    .header {
      padding: 16px 24px;
      border-bottom: 1px solid var(--surface-border);
      display: flex;
      align-items: center;
      justify-content: space-between;
      background: rgba(15, 23, 42, 0.4);
    }

    .header-left {
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .header-title {
      font-size: 18px;
      font-weight: 700;
      letter-spacing: -0.02em;
      display: flex;
      align-items: center;
      gap: 8px;
    }

    .header-sub {
      font-size: 12px;
      color: var(--text-muted);
    }

    .badge-pill {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 4px 10px;
      border-radius: 20px;
      font-size: 11px;
      font-weight: 600;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .badge-online {
      background: rgba(34, 197, 94, 0.15);
      color: #4ade80;
      border: 1px solid rgba(34, 197, 94, 0.3);
    }

    .header-right {
      display: flex;
      align-items: center;
      gap: 10px;
    }

    .btn-icon {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--surface-border);
      color: var(--text);
      padding: 8px 12px;
      border-radius: 12px;
      cursor: pointer;
      font-size: 13px;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all 0.2s;
    }

    .btn-icon:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.2);
    }

    /* Key Drawer / Settings bar */
    .key-bar {
      padding: 10px 24px;
      background: rgba(2, 6, 23, 0.6);
      border-bottom: 1px solid var(--surface-border);
      display: flex;
      align-items: center;
      gap: 12px;
      font-size: 13px;
    }

    .key-input {
      flex: 1;
      background: rgba(15, 23, 42, 0.8);
      border: 1px solid var(--surface-border);
      border-radius: 10px;
      color: var(--text);
      padding: 8px 14px;
      font-family: 'JetBrains Mono', monospace;
      font-size: 12px;
      outline: none;
      transition: border-color 0.2s;
    }

    .key-input:focus {
      border-color: var(--primary);
    }

    /* Chat Area */
    .chat-messages {
      flex: 1;
      overflow-y: auto;
      padding: 24px;
      display: flex;
      flex-direction: column;
      gap: 18px;
      scroll-behavior: smooth;
    }

    .message-row {
      display: flex;
      gap: 12px;
      max-width: 85%;
    }

    .message-row.user {
      align-self: flex-end;
      flex-direction: row-reverse;
    }

    .message-row.bot {
      align-self: flex-start;
    }

    .avatar {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
    }

    .avatar.bot {
      background: linear-gradient(135deg, #f59e0b, #d97706);
      border: 2px solid #fef08a;
    }

    .avatar.user {
      background: linear-gradient(135deg, #6366f1, #8b5cf6);
      border: 2px solid rgba(255, 255, 255, 0.3);
    }

    .bubble {
      padding: 14px 18px;
      border-radius: var(--radius);
      line-height: 1.55;
      font-size: 14.5px;
      position: relative;
      box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
    }

    .message-row.user .bubble {
      background: var(--card-user);
      color: #fff;
      border-bottom-right-radius: 4px;
    }

    .message-row.bot .bubble {
      background: var(--card-bot);
      border: 1px solid var(--surface-border);
      color: var(--text);
      border-bottom-left-radius: 4px;
    }

    /* Bot Meta Badges */
    .meta-tags {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 10px;
      padding-top: 10px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      font-size: 11px;
      font-family: 'JetBrains Mono', monospace;
      color: var(--text-muted);
    }

    .meta-tag {
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid rgba(255, 255, 255, 0.07);
      padding: 3px 8px;
      border-radius: 6px;
    }

    /* Suggestion Chips */
    .suggestions {
      display: flex;
      gap: 8px;
      overflow-x: auto;
      padding: 0 24px 12px;
      scrollbar-width: none;
    }

    .chip {
      background: rgba(255, 255, 255, 0.04);
      border: 1px solid var(--surface-border);
      color: var(--text-muted);
      padding: 6px 14px;
      border-radius: 20px;
      font-size: 12.5px;
      white-space: nowrap;
      cursor: pointer;
      transition: all 0.2s;
    }

    .chip:hover {
      background: rgba(56, 189, 248, 0.15);
      border-color: rgba(56, 189, 248, 0.4);
      color: #e0f2fe;
      transform: translateY(-1px);
    }

    /* Input Box */
    .input-box {
      padding: 16px 24px;
      border-top: 1px solid var(--surface-border);
      background: rgba(15, 23, 42, 0.6);
      display: flex;
      gap: 12px;
      align-items: center;
    }

    .input-field {
      flex: 1;
      background: rgba(255, 255, 255, 0.05);
      border: 1px solid var(--surface-border);
      border-radius: 16px;
      padding: 12px 18px;
      color: var(--text);
      font-size: 14.5px;
      outline: none;
      resize: none;
      max-height: 120px;
      transition: all 0.2s;
    }

    .input-field:focus {
      border-color: var(--primary);
      background: rgba(255, 255, 255, 0.08);
      box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.15);
    }

    .btn-send {
      background: linear-gradient(135deg, #38bdf8 0%, #2563eb 100%);
      color: white;
      border: none;
      width: 46px;
      height: 46px;
      border-radius: 14px;
      cursor: pointer;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s;
      flex-shrink: 0;
      box-shadow: 0 4px 15px rgba(37, 99, 235, 0.3);
    }

    .btn-send:hover {
      transform: scale(1.05);
      box-shadow: 0 6px 20px rgba(37, 99, 235, 0.45);
    }

    .btn-send:disabled {
      opacity: 0.5;
      cursor: not-allowed;
      transform: none;
    }

    /* Footer info */
    .footer-info {
      margin-top: 8px;
      font-size: 12px;
      color: var(--text-muted);
      text-align: center;
      display: flex;
      align-items: center;
      gap: 12px;
    }

    .footer-link {
      color: var(--primary);
      text-decoration: none;
    }
    .footer-link:hover {
      text-decoration: underline;
    }
  </style>
</head>
<body>

  <!-- Duck Cycling Banner Track -->
  <div class="duck-track">
    <div class="road-line"></div>
    <div class="cycling-duck-container" id="cyclingDuck">
      <!-- 2D SVG Cycling Duck -->
      <svg width="85" height="70" viewBox="0 0 100 80" fill="none" xmlns="http://www.w3.org/2000/svg">
        <!-- Back Wheel -->
        <g class="wheel" id="backWheel" style="transform-origin: 22px 60px;">
          <circle cx="22" cy="60" r="14" stroke="#94a3b8" stroke-width="3" fill="none"/>
          <line x1="22" y1="46" x2="22" y2="74" stroke="#94a3b8" stroke-width="1.5"/>
          <line x1="8" y1="60" x2="36" y2="60" stroke="#94a3b8" stroke-width="1.5"/>
          <circle cx="22" cy="60" r="3" fill="#38bdf8"/>
        </g>

        <!-- Front Wheel -->
        <g class="wheel" id="frontWheel" style="transform-origin: 75px 60px;">
          <circle cx="75" cy="60" r="14" stroke="#94a3b8" stroke-width="3" fill="none"/>
          <line x1="75" y1="46" x2="75" y2="74" stroke="#94a3b8" stroke-width="1.5"/>
          <line x1="61" y1="60" x2="89" y2="60" stroke="#94a3b8" stroke-width="1.5"/>
          <circle cx="75" cy="60" r="3" fill="#38bdf8"/>
        </g>

        <!-- Bike Frame -->
        <path d="M22 60 L45 60 L68 42 L38 42 Z" stroke="#38bdf8" stroke-width="3" stroke-linejoin="round" fill="none"/>
        <line x1="45" y1="60" x2="38" y2="35" stroke="#38bdf8" stroke-width="3"/>
        <line x1="68" y1="42" x2="75" y2="60" stroke="#38bdf8" stroke-width="3"/>
        <!-- Handlebars -->
        <path d="M68 42 L65 30 L72 30" stroke="#f1f5f9" stroke-width="2.5" stroke-linecap="round"/>
        <!-- Seat -->
        <path d="M32 35 L44 35" stroke="#f43f5e" stroke-width="4" stroke-linecap="round"/>

        <!-- Duck Character Group -->
        <g class="duck-body-group">
          <!-- Duck Tail -->
          <path d="M25 32 C20 30 22 25 28 27 Z" fill="#facc15"/>
          <!-- Duck Body -->
          <ellipse cx="40" cy="30" rx="13" ry="11" fill="#facc15"/>
          <!-- Duck Wing -->
          <path d="M35 32 C35 27 48 28 50 34 C46 36 38 36 35 32 Z" fill="#eab308"/>
          <!-- Duck Head -->
          <circle cx="50" cy="18" r="9" fill="#facc15"/>
          <!-- Duck Eye -->
          <circle cx="53" cy="16" r="2.2" fill="#0f172a"/>
          <circle cx="54" cy="15" r="0.8" fill="#ffffff"/>
          <!-- Duck Beak (Orange) -->
          <path d="M57 18 C64 19 65 23 56 23 Z" fill="#fb923c"/>
          <!-- Cyclist Helmet (Cyan) -->
          <path d="M42 16 C42 10 58 10 58 16 Z" fill="#06b6d4"/>
          <path d="M41 16 L61 16" stroke="#0891b2" stroke-width="2" stroke-linecap="round"/>
        </g>

        <!-- Pedals & Legs -->
        <g class="duck-leg">
          <line x1="40" y1="36" x2="45" y2="50" stroke="#ea580c" stroke-width="2.5" stroke-linecap="round"/>
          <circle cx="45" cy="50" r="2.5" fill="#f97316"/>
        </g>
        <g class="duck-leg-2">
          <line x1="40" y1="36" x2="35" y2="45" stroke="#c2410c" stroke-width="2.5" stroke-linecap="round"/>
          <circle cx="35" cy="45" r="2" fill="#ea580c"/>
        </g>
      </svg>
      <div class="duck-speech" id="duckSpeech">Quack! Vịt Cloud Agent đang đạp xe sẵn sàng! 🚲🦆</div>
    </div>
  </div>

  <!-- Main Chat Application Box -->
  <div class="app-container">
    <!-- Header -->
    <div class="header">
      <div class="header-left">
        <div class="header-title">
          <span>QuackBot AI</span>
          <span class="badge-pill badge-online" id="statusBadge">● Ready</span>
        </div>
        <div class="header-sub">K4-L3A-DAY12 • Ngô Tiến Dũng (L3A202602374)</div>
      </div>
      <div class="header-right">
        <button class="btn-icon" id="btnToggleKey" title="Cấu hình API Key">
          🔑 <span id="keyLabel">API Key</span>
        </button>
        <a href="/docs" target="_blank" class="btn-icon" style="text-decoration:none;">
          📚 Swagger Docs
        </a>
      </div>
    </div>

    <!-- API Key Input Bar -->
    <div class="key-bar" id="keyBar">
      <span style="color:var(--text-muted);">X-API-Key:</span>
      <input type="password" class="key-input" id="apiKeyInput" placeholder="Dán AGENT_API_KEY vào đây để trò chuyện..." />
      <button class="btn-icon" id="btnToggleShowKey" type="button" title="Hiện/Ẩn">👁️</button>
      <button class="btn-icon" id="btnSaveKey" style="background:#2563eb; color:#fff; border:none;">Lưu</button>
    </div>

    <!-- Messages Container -->
    <div class="chat-messages" id="chatMessages">
      <div class="message-row bot">
        <div class="avatar bot">🦆</div>
        <div class="bubble">
          Xin chào! Tôi là <b>QuackBot AI Agent</b> được xây dựng theo chuẩn 12-Factor, lưu trữ Stateless trên Redis và chạy Live trên Cloud Render! 🚲☁️<br><br>
          Bạn có thể bấm vào nút <b>🔑 API Key</b> ở góc trên để cấu hình khóa truy cập trước khi trò chuyện.
          <div class="meta-tags">
            <span class="meta-tag">⚡ Framework: FastAPI</span>
            <span class="meta-tag">🐳 Docker Multi-stage</span>
            <span class="meta-tag">🔴 Redis Key-Value</span>
          </div>
        </div>
      </div>
    </div>

    <!-- Quick Suggestions -->
    <div class="suggestions">
      <div class="chip" onclick="askQuestion('Deploy lên Cloud là gì?')">☁️ Deploy lên Cloud là gì?</div>
      <div class="chip" onclick="askQuestion('Tại sao Redis giúp service trở thành Stateless?')">🔴 Stateless với Redis</div>
      <div class="chip" onclick="askQuestion('Cơ chế Sliding Window Rate Limit hoạt động ra sao?')">🛡️ Sliding Window Rate Limit</div>
      <div class="chip" onclick="askQuestion('Cost Guard bảo vệ ngân sách thế nào?')">💰 Cost Guard LLM</div>
    </div>

    <!-- Input Form -->
    <form class="input-box" id="chatForm">
      <input type="text" class="input-field" id="questionInput" placeholder="Nhập câu hỏi để trò chuyện với Agent (Enter để gửi)..." autocomplete="off" />
      <button type="submit" class="btn-send" id="btnSend" title="Gửi câu hỏi">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
          <line x1="22" y1="2" x2="11" y2="13"></line>
          <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
        </svg>
      </button>
    </form>
  </div>

  <div class="footer-info">
    <span>Dự án: <a href="https://github.com/tiendungandrew-gif/K4-L3A-DAY12-NgoTienDung-L3A202602374-CloudServicesAndDeployment" target="_blank" class="footer-link">K4-L3A-DAY12 CloudServicesAndDeployment</a></span>
    <span>•</span>
    <span>Render URL: <a href="/health" target="_blank" class="footer-link">/health</a> | <a href="/ready" target="_blank" class="footer-link">/ready</a></span>
  </div>

  <script>
    const apiKeyInput = document.getElementById("apiKeyInput");
    const keyBar = document.getElementById("keyBar");
    const btnToggleKey = document.getElementById("btnToggleKey");
    const btnSaveKey = document.getElementById("btnSaveKey");
    const btnToggleShowKey = document.getElementById("btnToggleShowKey");
    const chatMessages = document.getElementById("chatMessages");
    const chatForm = document.getElementById("chatForm");
    const questionInput = document.getElementById("questionInput");
    const btnSend = document.getElementById("btnSend");
    const duckSpeech = document.getElementById("duckSpeech");
    const cyclingDuck = document.getElementById("cyclingDuck");
    const wheels = document.querySelectorAll(".wheel");

    // Init API Key from localStorage
    let storedKey = localStorage.getItem("AGENT_API_KEY") || "";
    apiKeyInput.value = storedKey;

    if (!storedKey) {
      keyBar.style.display = "flex";
      duckSpeech.innerText = "Quack! Dán API Key vào ô trên rồi bấm 'Lưu' nhé! 🔑";
    }

    btnToggleShowKey.addEventListener("click", () => {
      apiKeyInput.type = apiKeyInput.type === "password" ? "text" : "password";
    });

    btnToggleKey.addEventListener("click", () => {
      keyBar.style.display = keyBar.style.display === "none" ? "flex" : "none";
      if (keyBar.style.display === "flex") apiKeyInput.focus();
    });

    btnSaveKey.addEventListener("click", () => {
      storedKey = apiKeyInput.value.trim();
      localStorage.setItem("AGENT_API_KEY", storedKey);
      duckQuack("Đã lưu API Key an toàn trong trình duyệt! 🔑");
      keyBar.style.display = "none";
    });

    function duckQuack(text) {
      duckSpeech.innerText = text;
      // Animate duck faster briefly
      wheels.forEach(w => w.classList.add("fast"));
      setTimeout(() => {
        wheels.forEach(w => w.classList.remove("fast"));
      }, 1500);
    }

    // Move duck across track occasionally
    let duckPos = 20;
    setInterval(() => {
      duckPos = (duckPos + 60) % 650;
      cyclingDuck.style.left = `${duckPos}px`;
    }, 4000);

    // Health / Ready check
    async function checkSystem() {
      try {
        const res = await fetch("/ready");
        const data = await res.json();
        const badge = document.getElementById("statusBadge");
        if (data.status === "ready" && data.redis) {
          badge.className = "badge-pill badge-online";
          badge.innerText = "● Ready & Redis Connected";
        } else {
          badge.className = "badge-pill";
          badge.style.background = "#ef444422";
          badge.style.color = "#f87171";
          badge.innerText = "● Degraded";
        }
      } catch (err) {
        console.warn("Ready check failed:", err);
      }
    }
    checkSystem();

    function appendMessage(text, role, meta = null) {
      const row = document.createElement("div");
      row.className = `message-row ${role}`;
      
      const avatar = document.createElement("div");
      avatar.className = `avatar ${role}`;
      avatar.innerHTML = role === "user" ? "👤" : "🦆";

      const bubble = document.createElement("div");
      bubble.className = "bubble";
      bubble.innerText = text;

      if (meta) {
        const tags = document.createElement("div");
        tags.className = "meta-tags";
        tags.innerHTML = `
          <span class="meta-tag">🧠 History: ${meta.history_length} msgs</span>
          <span class="meta-tag">⚡ Tokens: ${meta.tokens?.in || 0} in / ${meta.tokens?.out || 0} out</span>
          <span class="meta-tag">💰 Cost: $${(meta.cost_usd || 0).toFixed(6)}</span>
        `;
        bubble.appendChild(tags);
      }

      row.appendChild(avatar);
      row.appendChild(bubble);
      chatMessages.appendChild(row);
      chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async function askQuestion(question) {
      if (!question || question.trim() === "") return;
      question = question.trim();

      if (!storedKey) {
        keyBar.style.display = "flex";
        apiKeyInput.focus();
        appendMessage("🔑 Bạn cần nhập API Key để bắt đầu trò chuyện. Hãy dán AGENT_API_KEY vào ô trên thanh công cụ rồi bấm 'Lưu' nhé!", "bot");
        duckQuack("Quack! Cần có API Key mới gọi được Agent! 🔑");
        return;
      }

      questionInput.value = "";
      appendMessage(question, "user");
      btnSend.disabled = true;
      duckQuack("Đang đạp xe tìm câu trả lời cho bạn... 🚲💨");

      const loadingRow = document.createElement("div");
      loadingRow.className = "message-row bot";
      loadingRow.id = "loadingMsg";
      loadingRow.innerHTML = `
        <div class="avatar bot">🦆</div>
        <div class="bubble" style="color:var(--text-muted); font-style:italic;">
          Vịt đang suy nghĩ và tính toán token...
        </div>
      `;
      chatMessages.appendChild(loadingRow);
      chatMessages.scrollTop = chatMessages.scrollHeight;

      try {
        const res = await fetch("/ask", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-API-Key": storedKey,
            "X-User-Id": "web-user"
          },
          body: JSON.stringify({ question })
        });

        const loadingElem = document.getElementById("loadingMsg");
        if (loadingElem) loadingElem.remove();

        if (res.status === 200) {
          const data = await res.json();
          appendMessage(data.answer, "bot", data);
          duckQuack(`Quack! Xong rồi, tiêu tốn $${data.cost_usd.toFixed(6)} USD!`);
        } else if (res.status === 401) {
          appendMessage("❌ Lỗi 401: API Key không hợp lệ hoặc bị thiếu! Vui lòng bấm vào nút 'API Key' ở góc trên để cấu hình khóa hợp lệ.", "bot");
          duckQuack("Quack! Thiếu hoặc sai API Key rồi bạn ơi! 🚫");
        } else if (res.status === 429) {
          appendMessage("⚠️ Lỗi 429: Bạn đã vượt quá giới hạn Rate Limit (10 req/phút) hoặc vượt hạn mức ngân sách tháng! Vui lòng thử lại sau.", "bot");
          duckQuack("Quack quack! Đi chậm lại nào, bị dính Rate Limit rồi! 🛑");
        } else {
          const errData = await res.json().catch(() => ({}));
          appendMessage(`❌ Lỗi ${res.status}: ${errData.detail || "Không thể gọi tới agent."}`, "bot");
        }
      } catch (err) {
        const loadingElem = document.getElementById("loadingMsg");
        if (loadingElem) loadingElem.remove();
        appendMessage(`❌ Lỗi kết nối: ${err.message}`, "bot");
        duckQuack("Quack! Không kết nối được tới server! 🔌");
      } finally {
        btnSend.disabled = false;
        questionInput.focus();
      }
    }

    chatForm.addEventListener("submit", (e) => {
      e.preventDefault();
      askQuestion(questionInput.value);
    });
  </script>
</body>
</html>
"""

