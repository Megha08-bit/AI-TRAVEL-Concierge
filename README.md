# ✈️ AI Travel Concierge
### Intelligent AI-Powered Travel Planning Assistant

[![Python](https://img.shields.io/badge/Python-3.11+-blue?style=for-the-badge&logo=python)](https://python.org)
[![LangChain](https://img.shields.io/badge/LangChain-Latest-green?style=for-the-badge)](https://langchain.com)
[![Groq](https://img.shields.io/badge/LLM-Groq_LLaMA_3.3-orange?style=for-the-badge)](https://groq.com)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-red?style=for-the-badge&logo=streamlit)](https://streamlit.io)
[![SQLite](https://img.shields.io/badge/Database-SQLite-blue?style=for-the-badge&logo=sqlite)](https://sqlite.org)

---

## 🚀 Live Demo

👉 **[Click here to try the app](https://ai-tavel-concierge.streamlit.app/)**

---

## 📌 Project Overview

**AI Travel Concierge** is an intelligent travel planning assistant built with **LangChain**, **Groq LLaMA 3.3**, and **Streamlit**. It helps users plan complete trips using real-world APIs and AI reasoning — from generating day-wise itineraries to estimating budgets, checking weather across 240+ cities worldwide, and converting currencies in real time.

---

## 🖥️ Screenshots

| Chat Interface | Trip Planner | Weather & Currency |
|:-:|:-:|:-:|
| AI-powered travel chat | Day-wise itinerary + budget | 240+ city weather + live rates |

<img width="1920" height="1080" alt="Screenshot (374)" src="https://github.com/user-attachments/assets/cf4b35ad-61fc-4a1a-8139-2fb201f6805b" />
<img width="1920" height="1080" alt="Screenshot (375)" src="https://github.com/user-attachments/assets/fa698bb4-2f6d-4e33-85ba-ba4966bfb2d5" />
<img width="1920" height="1080" alt="Screenshot (376)" src="https://github.com/user-attachments/assets/64249957-0e6b-4904-9395-9d06f208c205" />
<img width="1920" height="1080" alt="Screenshot (390)" src="https://github.com/user-attachments/assets/715672d7-55ae-4962-9d55-3e42b8ff9183" />
<img width="1920" height="1080" alt="Screenshot (378)" src="https://github.com/user-attachments/assets/84c2b41e-1fce-47ea-8bc1-b287d9e4d890" />
<img width="1920" height="1080" alt="Screenshot (379)" src="https://github.com/user-attachments/assets/f26a5b47-dbb0-4246-b076-53ad98e6ba68" />
<img width="1920" height="1080" alt="Screenshot (380)" src="https://github.com/user-attachments/assets/35918eff-30a3-4b8a-8f4f-ae95e37dae4a" />
<img width="1920" height="1080" alt="Screenshot (381)" src="https://github.com/user-attachments/assets/0ba6f43b-dfd7-449d-9235-ca1c9d00a79f" />
<img width="1920" height="1080" alt="Screenshot (382)" src="https://github.com/user-attachments/assets/8cfa1a19-ee37-45db-8a43-3d8dfa12f0c2" />
<img width="1920" height="1080" alt="Screenshot (383)" src="https://github.com/user-attachments/assets/1d29dda6-e0a0-4607-8fe9-26f0914f6f62" />
<img width="1920" height="1080" alt="Screenshot (385)" src="https://github.com/user-attachments/assets/6fa00939-f0c2-440b-80d4-7e7132b847b0" />



---

## 🌟 Key Features

| Feature | Description |
|---------|-------------|
| 💬 **AI Chat** | Natural language travel Q&A powered by Groq LLaMA 3.3 |
| 🗓️ **Trip Planner** | Day-wise itinerary generator for any destination |
| 💰 **Budget Estimator** | Detailed cost breakdown for 25+ destinations |
| 🌤️ **Weather Check** | Real-time weather for 240+ cities worldwide |
| 💱 **Currency Converter** | Live exchange rates via ExchangeRate API |
| 📚 **Travel Knowledge Base** | RAG-powered knowledge on visas, packing, destinations |
| 💾 **History** | SQLite database saves all searches and itineraries |
| 📥 **Export** | Download complete trip plans as text files |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│                   Streamlit UI                   │
│  Chat | Trip Planner | Weather | History | About │
└──────────────────────┬──────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────┐
│              LangChain Agent                     │
│         (Tool Binding + Groq LLM)               │
└──────┬───────┬───────┬──────┬───────────────────┘
       │       │       │      │
  ┌────▼─┐ ┌──▼──┐ ┌──▼──┐ ┌─▼──────┐ ┌─────────┐
  │Weath-│ │Curr-│ │SERP │ │Itiner- │ │ Budget  │
  │ er   │ │ency │ │ API │ │  ary   │ │Estimato │
  │ API  │ │ API │ │     │ │        │ │    r    │
  └──────┘ └─────┘ └─────┘ └────────┘ └─────────┘
                       │
           ┌───────────▼──────────┐
           │    SQLite Database   │
           │ search_history       │
           │ itineraries          │
           └──────────────────────┘
```

---

## 🛠️ Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **LLM** | Groq LLaMA 3.3-70b | AI language model |
| **Agent Framework** | LangChain | Tool binding & agent logic |
| **RAG** | FAISS + HuggingFace Embeddings | Knowledge retrieval |
| **Database** | SQLite | Persistent storage |
| **UI** | Streamlit | Web interface |
| **Deployment** | Streamlit Cloud | Hosting |
| **Language** | Python 3.11+ | Core language |

---

## 🔑 APIs Used

| API | Purpose |
|-----|---------|
| [Groq](https://console.groq.com) | LLM (LLaMA 3.3) | 
| [SERP API](https://serpapi.com) | Flight & Hotel search | 
| [Weatherstack](https://weatherstack.com) | Weather data | 
| [ExchangeRate-API](https://exchangerate-api.com) | Currency rates | 

---

## 🗂️ Project Structure

```
ai-travel-concierge/
│
├── app.py                  ← Main Streamlit app (ALL weeks combined)           (frontend)
├── agent.py                ← LLM and class                                     (backend)
├── tools.py                ← wheather,currency,hotels,flights,web search tools (backend)
├── database.py             ← SQLite operations                                 (backend)
├── rag_pipeline.py         ← RAG                                               (backend)
├── requirements.txt        ← Python dependencies
├── README.md               ← This file
├── .gitignore              ← Files excluded from Git
│
└── notebooks                ← Weekly development notebook
  └──aitravelconcierge1-8.py 

    

```

---

## 📅 8-Week Development Timeline

### ✅ Week 1-2: Foundation & RAG Chatbot
- Set up LangChain + Groq LLM
- Built RAG knowledge base (FAISS + HuggingFace embeddings)
- Travel knowledge: visas, packing, destinations, flight tips, India travel
- Basic Gradio chat interface
- **Milestone:** Working deployed demo

### ✅ Week 3-4: Core Agent Architecture
- Built LangChain agent with `bind_tools()`
- Integrated 5 real API tools:
  - 🌤️ Weather Tool (240+ cities)
  - 💱 Currency Converter (live rates)
  - ✈️ Flight Search (SERP API)
  - 🏨 Hotel Search (SERP API)
  - 🔍 General Travel Web Search
- **Milestone:** Agent uses multiple tools correctly

### ✅ Week 5-6: Domain Specialization
- Day-wise Itinerary Generator (LLM-powered)
- Budget Estimator (25+ destinations)
- SQLite database (saves searches + itineraries)
- Full multi-tab Gradio UI
- **Milestone:** Complete travel planning app

### ✅ Week 7-8: Polish & Production
- Automated testing suite (5 test cases)
- Export feature (download trip plans)
- Error handling + fallback mechanisms
- Deployed to Streamlit Cloud
- **Milestone:** Production-ready deployed application

---

## 🚀 How to Run

### Option 1: Streamlit Cloud (Deployed)
**Visit the live app(https://ai-tavel-concierge.streamlit.app/)**

### Option 2: Google Colab
1. Open any notebook from the `notebooks/` folder in Google Colab
2. Click 🔑 **Secrets** (left sidebar) → add your API keys:
   ```
   GROQ_API_KEY
   SERP_API_KEY
   WEATHERSTACK_API_KEY
   EXCHANGERATE_API_KEY
   ```
3. Run all cells from top to bottom
4. Click the Gradio public link

### Option 3: Run Locally
```bash
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/ai-travel-concierge.git
cd ai-travel-concierge

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file with your API keys
echo "GROQ_API_KEY=your_key_here" > .env
echo "SERP_API_KEY=your_key_here" >> .env
echo "WEATHERSTACK_API_KEY=your_key_here" >> .env
echo "EXCHANGERATE_API_KEY=your_key_here" >> .env

# 4. Run the app
streamlit run app.py
```

---

## 🌍 Weather Coverage

The app includes weather data for **240+ cities** across **50+ countries**:

| Region | Coverage |
|--------|----------|
| 🇮🇳 **India** | 90+ cities — all 28 states + UTs |
| 🌏 **Asia Pacific** | 50+ cities (Japan, SE Asia, China, Australia) |
| 🌍 **Europe** | 60+ cities (UK, France, Germany, Italy, Spain...) |
| 🌎 **Americas** | 30+ cities (USA, Canada, Latin America) |
| 🌐 **Middle East & Africa** | 25+ cities |

**Indian states covered:**
Andhra Pradesh, Assam, Bihar, Chhattisgarh, Goa, Gujarat, Haryana,
Himachal Pradesh, Jharkhand, Karnataka, Kerala, Madhya Pradesh,
Maharashtra, Meghalaya, Odisha, Punjab, Rajasthan, Tamil Nadu,
Telangana, Uttar Pradesh, Uttarakhand, West Bengal, Delhi, J&K,
Ladakh, Andaman Islands and more!

---

## 💬 Example Conversations

```
You: Plan a 5-day Bali trip for 2 people on mid-range budget
Bot: 🗺️ 5-DAY BALI ITINERARY
     Day 1: South Kuta Beach
     - Morning: Breakfast at Naughty Nuri's ($5/person)...
     - Estimated daily cost: $60-80

You: What's the weather in Shimla right now?
Bot: Shimla — 12°C / 54°F
     Condition: Cool & Cloudy | Humidity: 65%
     Tip: Mild, carry a light jacket.

You: Convert 1000 USD to Indian Rupees
Bot: 1,000.00 USD = 83,500.00 INR
     Rate: 1 USD = 83.5000 INR

You: Visa requirements for Japan from India
Bot: Indian citizens require a visa for Japan...
     [detailed visa process + costs]
```



## 🧪 Automated Tests

The project includes an automated test suite (Week 7-8):

```
✅ Weather Test      — Real-time weather retrieval
✅ Currency Test     — Live exchange rate conversion
✅ Budget Test       — Trip cost estimation
✅ Itinerary Test    — Day-wise plan generation
✅ Search Test       — Visa & travel info search

Score: 5/5 tests passed | Avg response: ~3.2s
```
---

## 🔮 Future Improvements 

- [ ] Migrate to LangGraph for complex agent workflows
- [ ] Add FastAPI backend + React frontend
- [ ] PostgreSQL + Redis for production database
- [ ] Real-time flight prices via Amadeus API
- [ ] Voice input/output capabilities
- [ ] Multi-language support
- [ ] CI/CD pipeline with GitHub Actions
- [ ] Performance monitoring dashboard

---

## 📝 Lessons Learned

- **LangChain versioning** — APIs change frequently; `bind_tools()` is the stable modern approach
- **Groq vs Gemini** — Groq is more reliable for free-tier usage with fewer quota issues
- **RAG implementation** — HuggingFace embeddings work well without API key dependency
- **Streamlit deployment** — Simple but powerful; secrets management is straightforward
- **Error handling** — Always add fallbacks for API failures in production

---

## 👨‍💻 Author

- *Team Name*: Mind Matrix
- *Project*: AI Travel Concierge
- *Track*: Track A (Essential)
- *Duration*: 8 Weeks
- *Platform*: Google Colab

---


*Built with  using LangChain + Groq + Streamlit*
