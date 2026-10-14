# ⚖️ VakilBot — Indian Legal Help Bot

An AI-powered legal assistant for Indian citizens, providing guidance on publicly available Indian laws using **RAG (Retrieval-Augmented Generation)** with **Google Gemini** and **ChromaDB**.

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 **AI Engine** | Google Gemini 2.5 Flash / 1.5 Flash with RAG |
| 📚 **Indian Legal Coverage** | Constitution, BNS/IPC, BNSS, Consumer Protection, RTI, Cyber, Family & Labour Laws |
| 🔍 **Dual RAG Engine** | ChromaDB (local) + Lightweight In-Memory Semantic Retriever (Vercel serverless) |
| 🌐 **Multilingual Support** | 16 Languages (Hindi, Bengali, Tamil, Telugu, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Spanish, French, German, Arabic, Russian, English) |
| 🎓 **Adaptive Knowledge Levels** | 3 User Modes: `🌱 New to Law`, `⚖️ Intermediate`, `🎓 Expert / Advocate` |
| 📖 **Interactive Legal Glossary** | Hover tooltips on desktop + slide-up touch sheets on mobile for legal terms (*BNSS*, *Bail*, *FIR*, etc.) |
| ♿ **WCAG AAA Accessibility** | High-contrast black/gold mode, OpenDyslexic readable font, 3-tier font size scaler |
| 🎙️ **Voice STT & TTS** | Speech-to-Text microphone input + Text-to-Speech audio read-aloud |
| 📱 **Responsive Restructuring** | Tailored UI architectures for Desktop (`1440px`), Tablet (`768px–1024px`), and Mobile (`360px–480px`) |
| ⚡ **Vercel Serverless Ready** | Native `vercel.json` and `api/index.py` for instant 1-click cloud deployment |


---

## 🚀 Quick Start

### 1. Get a Free Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click **"Create API Key"** → it's free!

### 2. Set Up the API Key
```powershell
# Copy the example env file
Copy-Item backend\.env.example backend\.env

# Edit backend\.env and set your key:
# GEMINI_API_KEY=your_actual_api_key_here
```

### 3. Install Dependencies
```powershell
cd backend
py -3 -m pip install -r requirements.txt
```

### 4. Start the Bot
```powershell
# Option A: Double-click start.bat
# Option B: PowerShell
cd backend
py -3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

### 5. Open in Browser
Navigate to: **http://localhost:8000**

---

## 📁 Project Structure

```
legal-bot/
├── backend/
│   ├── main.py            # FastAPI app (routes, API)
│   ├── rag_engine.py      # RAG pipeline (Gemini + ChromaDB)
│   ├── knowledge_base.py  # Indian legal knowledge base
│   ├── requirements.txt   # Python dependencies
│   └── .env               # Your API keys (create from .env.example)
├── frontend/
│   └── index.html         # Chat UI
├── data/
│   └── chroma_db/         # Vector store (auto-created)
├── setup.py               # Setup & validation script
├── start.bat              # Windows one-click starter
└── README.md
```

---

## 📋 Legal Coverage

| Category | Topics Covered |
|---|---|
| ⚖️ **Fundamental Rights** | Articles 14, 19, 21, 22, 32, 39A |
| 🔒 **Criminal Law** | BNS/IPC sections — murder, rape, theft, fraud, defamation |
| 👨‍👩‍👧 **Family Law** | Divorce, custody, domestic violence (PWDVA) |
| 🛒 **Consumer Law** | Consumer Protection Act 2019, e-commerce complaints |
| 💻 **Cyber Law** | IT Act, cybercrime reporting (1930 helpline) |
| 👷 **Labour Law** | Wages, POSH Act, maternity leave, gratuity |
| 🏠 **Property Law** | Tenant rights, land acquisition, registration |
| 📋 **RTI** | Filing process, PIO, appeals, penalties |
| 🤝 **Legal Aid** | NALSA, DLSA, Lok Adalat, free lawyers |
| 🚔 **Criminal Procedure** | FIR rights, bail, arrest rights |
| 👶 **Child Protection** | POCSO Act 2012 |

---

## 🆘 Emergency Helplines

| Service | Number |
|---|---|
| Police | 100 |
| Women Helpline | 1091 |
| Child Helpline | 1098 |
| Cybercrime | **1930** |
| National Legal Aid | **15100** |
| Consumer Helpline | 1800-11-4000 |
| Ambulance | 102 |

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serve frontend |
| `GET` | `/health` | Service health check |
| `POST` | `/chat` | Main legal Q&A |
| `GET` | `/categories` | List legal categories |
| `GET` | `/sample-questions` | Get sample questions |
| `POST` | `/refresh-kb` | Rebuild vector store |
| `GET` | `/docs` | Interactive API docs (Swagger) |

---

## ⚠️ Disclaimer

VakilBot provides **general legal information** based on publicly available Indian laws. It is **not a substitute** for professional legal advice. For serious legal matters, please consult a qualified advocate. The information may not reflect the most recent amendments.

---

## 🤝 Free Legal Resources

- **NALSA**: [nalsa.gov.in](https://nalsa.gov.in) | 📞 15100
- **Consumer Forum**: [edaakhil.nic.in](https://edaakhil.nic.in)
- **Cybercrime Portal**: [cybercrime.gov.in](https://cybercrime.gov.in)
- **RBI Ombudsman**: [cms.rbi.org.in](https://cms.rbi.org.in)
- **SEBI SCORES**: [scores.gov.in](https://scores.gov.in)
- **eCourts**: [ecourts.gov.in](https://ecourts.gov.in)
