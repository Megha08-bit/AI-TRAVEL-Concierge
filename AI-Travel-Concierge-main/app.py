# ============================================================
# app.py  — Streamlit Frontend  (root file for Streamlit Cloud)
# AI Travel Concierge — All 8 Weeks combined
# ============================================================
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="AI Travel Concierge",
    page_icon="✈️",
    layout="wide",
)

# ── Bootstrap imports ─────────────────────────────────────────
from agent       import load_llm, build_executor, get_model_name
from tools       import ALL_TOOLS, CITY_WEATHER, DESTINATION_COSTS
from rag_pipeline import build_rag_chain, rag_chat, TRAVEL_KNOWLEDGE
from database    import init_database, save_search, get_search_history, get_saved_itineraries
from agent       import EXCHANGERATE_API_KEY

# ── One-time init ─────────────────────────────────────────────
init_database()

# ── LLM + Agent (cached so Streamlit doesn't reload on every rerun) ──
@st.cache_resource
def get_agent():
    _llm, _model = load_llm()
    if _llm is None:
        return None, None, None, None
    _executor, _tool_map = build_executor(ALL_TOOLS)
    return _llm, _model, _executor, _tool_map

llm, model_name, agent_executor, tool_map = get_agent()

# ── RAG chain (Week 1-2) ──────────────────────────────────────
@st.cache_resource
def get_rag_chain():
    if llm is None:
        return None
    return build_rag_chain(llm)

rag_chain = get_rag_chain()

# ── Helper: weather ──────────────────────────────────────────
def weather_info(city: str) -> str:
    clow = city.lower().strip()
    if clow in CITY_WEATHER:
        w  = CITY_WEATHER[clow]
        t  = w["temp"]; tf = round(t * 9/5 + 32)
        if t >= 35:   tip = "Very hot! Carry water and sunscreen."
        elif t >= 28: tip = "Warm! Light clothes recommended."
        elif t >= 20: tip = "Great weather for sightseeing!"
        elif t >= 12: tip = "Mild, carry a light jacket."
        else:         tip = "Cold! Pack warm clothes."
        if "rain" in w["desc"].lower(): tip += " Carry an umbrella!"
        save_search("weather", city, f"{t}°C {w['desc']}")
        return (
            f"**{city.title()}** — {t}°C / {tf}°F\n\n"
            f"- Feels like: {w['feel']}°C\n"
            f"- Condition : {w['desc']}\n"
            f"- Humidity  : {w['humidity']}%\n"
            f"- Wind      : {w['wind']} km/h\n\n"
            f"**Tip:** {tip}"
        )
    return f"**{city.title()}** — not in database. Check weather.com"


# ── Helper: currency ─────────────────────────────────────────
def currency_info(amount: float, fr: str, to: str) -> str:
    try:
        r = requests.get(
            f"https://v6.exchangerate-api.com/v6/{EXCHANGERATE_API_KEY}/pair/{fr}/{to}/{amount}",
            timeout=10,
        ).json()
        if r.get("result") == "success":
            save_search("currency", f"{amount} {fr} {to}", f"{r['conversion_result']:,.2f} {to}")
            return (
                f"**{amount:,.2f} {fr} = {r['conversion_result']:,.2f} {to}**\n\n"
                f"Rate: 1 {fr} = {r['conversion_rate']:.4f} {to}\n\n"
                f"- Avoid airport exchange (poor rates)\n"
                f"- Use Wise / Revolut for transfers\n"
                f"- Always carry some local cash"
            )
        fallback = {
            ("USD","INR"):83.5,("EUR","INR"):90.2,
            ("USD","JPY"):149.5,("GBP","INR"):105.8,
        }
        rate = fallback.get((fr, to))
        if rate:
            return f"~{amount * rate:,.2f} {to}  (offline approximate rate)"
        return f"Could not convert {fr} to {to}"
    except Exception:
        return "Currency service unavailable. Try xe.com"


# ── Helper: budget ───────────────────────────────────────────
def budget_info(destination: str, days: int, budget: str, travelers: int) -> str:
    dk = destination.lower()
    if dk not in DESTINATION_COSTS:
        dk = next((k for k in DESTINATION_COSTS if k in dk or dk in k), "default")
    costs  = DESTINATION_COSTS.get(dk, DESTINATION_COSTS["default"])
    if budget not in costs: budget = "mid-range"
    daily  = costs[budget]; per_pp = daily * days; total = per_pp * travelers
    save_search("budget", f"{destination} {days}d {budget}", f"${total:.0f}")
    return (
        f"**{destination.title()}** | {days} days | {budget.title()} | {travelers} traveler(s)\n\n"
        f"---\n**Daily/person:** ~${daily}\n\n"
        f"**Per person (${per_pp:,.0f}):**\n"
        f"- Accommodation: ${per_pp*0.35:,.0f}\n"
        f"- Food: ${per_pp*0.25:,.0f}\n"
        f"- Activities: ${per_pp*0.20:,.0f}\n"
        f"- Transport: ${per_pp*0.10:,.0f}\n"
        f"- Misc: ${per_pp*0.10:,.0f}\n\n"
        f"**Total ({travelers} person(s)):** ${total:,.0f} *(excl. flights)*\n"
        f"**With flights:** ${total+600*travelers:,.0f} – ${total+1400*travelers:,.0f}\n\n"
        f"*Tip: Travel shoulder season to save 10-30%!*"
    )


# ── Helper: chat ─────────────────────────────────────────────
def chat_response(question: str) -> str:
    if agent_executor is None:
        return "Agent not available. Check API keys in Streamlit Secrets."
    return agent_executor.invoke({"input": question})["output"]


# ── Helper: export ────────────────────────────────────────────
def export_trip(destination: str, days: int, budget: str, travelers: int,
                itinerary: str, budget_text: str) -> str:
    return (
        f"AI TRAVEL CONCIERGE — TRIP PLAN\n"
        f"Generated : {datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
        f"LLM       : Groq ({model_name})\n"
        + "="*60 + "\n\n"
        f"DESTINATION : {destination.title()}\n"
        f"DAYS        : {days}\n"
        f"BUDGET      : {budget.title()}\n"
        f"TRAVELERS   : {travelers}\n\n"
        f"ITINERARY\n{itinerary}\n\n"
        f"BUDGET ESTIMATE\n{budget_text}\n\n"
        f"Powered by Groq + LangChain\n"
    )


# =============================================================
# PAGE HEADER
# =============================================================
st.title("✈️ AI Travel Concierge")
st.markdown(
    f"Intelligent AI-Powered Travel Planning Assistant")
st.divider()

# =============================================================
# TABS
# =============================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "💬 Chat",
    "🗓️ Trip Planner",
    "🌤️ Weather & Currency",
    "📚 Travel Knowledge",
    "💾 History",
    "ℹ️ About",
])

# ════════════════════════════════════════════════════
# TAB 1 — CHAT   (Weeks 3-8)
# ════════════════════════════════════════════════════
with tab1:
    st.subheader("Chat with TravelBot")

    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [{
            "role"   : "assistant",
            "content": (
                "👋 Hello! I'm TravelBot, your AI Travel Concierge!\n\n"
                "I can help with:\n"
                "✈️ Flights  |  🏨 Hotels  |  🌤️ Weather\n"
                "🗓️ Itineraries  |  💰 Budgets  |  💱 Currency\n\n"
                "*Try: Plan a 5-day Bali trip for 2 people mid-range budget*"
            ),
        }]

    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    st.markdown("**💡 Quick prompts:**")
    qc1, qc2, qc3 = st.columns(3)
    prompts = [
        "Plan 5-day Bali trip 2 people budget",
        "Best time to visit Japan?",
        "Budget for 7 days in Europe?",
        "Visa for Dubai from India",
        "Top things to do in Paris",
        "Cheap flight booking tips",
    ]
    for i, p in enumerate(prompts):
        if [qc1, qc2, qc3][i % 3].button(p, key=f"qp_{i}", use_container_width=True):
            st.session_state._pending = p
            st.rerun()

    if "_pending" in st.session_state:
        user_input = st.session_state._pending
        del st.session_state._pending
    else:
        user_input = st.chat_input("Ask anything about travel...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.write(user_input)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = chat_response(user_input)
            st.write(response)
        st.session_state.chat_history.append({"role": "assistant", "content": response})

# ════════════════════════════════════════════════════
# TAB 2 — TRIP PLANNER   (Weeks 5-8)
# ════════════════════════════════════════════════════
with tab2:
    st.subheader("🗓️ Plan Your Perfect Trip")
    st.caption("Get a complete day-wise itinerary + full budget breakdown instantly!")

    col_l, col_r = st.columns([1, 2])

    with col_l:
        dest      = st.text_input("🌍 Destination", placeholder="e.g. Bali, Tokyo, Paris")
        days      = st.slider("📅 Days", 1, 14, 5)
        budget    = st.radio("💰 Budget", ["budget", "mid-range", "luxury"], index=1)
        travelers = st.slider("👥 Travelers", 1, 10, 2)

        c1, c2   = st.columns(2)
        plan_btn = c1.button("🗓️ Plan Trip!", type="primary", use_container_width=True)
        cost_btn = c2.button("💰 Estimate Cost", use_container_width=True)

        # Week 7-8: Export feature
        st.divider()
        exp_btn = st.button("📥 Export Full Plan", use_container_width=True)
        if exp_btn and dest:
            with st.spinner("Generating full plan..."):
                from tools import generate_itinerary, estimate_budget
                itin_txt = generate_itinerary.invoke(f"{dest} {days} {budget} {travelers}")
                bud_txt  = estimate_budget.invoke(f"{dest} {days} {budget} {travelers}")
            content = export_trip(dest, days, budget, travelers, itin_txt, bud_txt)
            st.download_button(
                "💾 Download Trip Plan (.txt)",
                data=content,
                file_name=f"{dest}_{days}day_plan.txt",
                mime="text/plain",
                use_container_width=True,
            )

    with col_r:
        itin_tab, bud_tab = st.tabs(["📍 Itinerary", "💰 Budget"])

        if plan_btn and dest:
            with itin_tab:
                with st.spinner(f"Creating {days}-day {dest} itinerary..."):
                    from tools import generate_itinerary
                    st.write(generate_itinerary.invoke(f"{dest} {days} {budget} {travelers}"))

        if cost_btn and dest:
            with bud_tab:
                st.markdown(budget_info(dest, days, budget, travelers))

        if (plan_btn or cost_btn) and not dest:
            st.warning("⚠️ Please enter a destination first!")

        if not plan_btn and not cost_btn:
            st.info("👈 Fill in the details on the left and click Plan Trip! or Estimate Cost")

# ════════════════════════════════════════════════════
# TAB 3 — WEATHER & CURRENCY   (Week 3-4)
# ════════════════════════════════════════════════════
with tab3:
    wc1, wc2 = st.columns(2)

    with wc1:
        st.subheader("🌤️ Weather Check")
        st.caption("240+ cities worldwide including all Indian states")
        city = st.text_input("Enter city:", placeholder="e.g. Tokyo, Bali, Shimla, Leh")
        if st.button("Get Weather", type="primary", use_container_width=True):
            st.info(weather_info(city) if city else "Please enter a city name!")

        st.markdown("**Quick cities:**")
        qcols = st.columns(4)
        for i, c in enumerate(["Tokyo","Bali","Paris","Dubai","Mumbai","Shimla","Leh","Goa"]):
            if qcols[i % 4].button(c, key=f"wc_{i}", use_container_width=True):
                st.info(weather_info(c))

    with wc2:
        st.subheader("💱 Currency Converter")
        amount    = st.number_input("Amount:", value=100.0, min_value=0.01)
        cc1, cc2  = st.columns(2)
        from_curr = cc1.selectbox("From:", ["USD","EUR","GBP","INR","JPY","AUD","SGD","THB","CAD"])
        to_curr   = cc2.selectbox("To:",   ["INR","USD","EUR","JPY","GBP","THB","SGD","AUD","CAD"])
        if st.button("Convert 💱", type="primary", use_container_width=True):
            st.success(currency_info(amount, from_curr, to_curr))

# ════════════════════════════════════════════════════
# TAB 4 — TRAVEL KNOWLEDGE   (Week 1-2 RAG)
# ════════════════════════════════════════════════════
with tab4:
    st.subheader("📚 Travel Knowledge Base")
    st.caption(
        "Week 1-2: RAG-powered knowledge on visas, packing, "
        "destinations, India travel, flights, hotels and more."
    )

    rag_q = st.text_input(
        "Ask the knowledge base:",
        placeholder="e.g. What documents do I need for international travel?"
    )
    if st.button("Search Knowledge Base", type="primary"):
        if rag_q:
            with st.spinner("Searching..."):
                if rag_chain:
                    answer = rag_chat(rag_q, rag_chain)
                else:
                    from langchain_core.messages import HumanMessage, SystemMessage
                    kb = "\n\n".join(TRAVEL_KNOWLEDGE)
                    resp = llm.invoke([
                        SystemMessage(content=f"You are a travel expert. Use this knowledge:\n\n{kb}"),
                        HumanMessage(content=rag_q),
                    ])
                    answer = resp.content
                save_search("rag", rag_q, answer[:200])
                st.info(answer)
        else:
            st.warning("Please enter a question!")

    st.divider()
    st.markdown("**📋 Topics in the knowledge base:**")
    topics = [
        "🛂 Visa Information",
        "💰 Travel Budget Tips",
        "🎒 Packing Essentials",
        "🌍 Top Destinations 2024",
        "🇮🇳 India Travel Guide",
        "✈️ Flight Booking Tips",
        "🏨 Hotel Booking Tips",
    ]
    tc1, tc2 = st.columns(2)
    for i, t in enumerate(topics):
        (tc1 if i % 2 == 0 else tc2).info(t)

# ════════════════════════════════════════════════════
# TAB 5 — HISTORY   (Week 5-6 SQLite)
# ════════════════════════════════════════════════════
with tab5:
    st.subheader("💾 Your Saved Data")
    st.caption("All searches and itineraries are saved automatically in a SQLite database.")

    h1, h2 = st.columns(2)

    with h1:
        st.markdown("### 📋 Recent Searches")
        if st.button("🔄 Load History", use_container_width=True):
            rows = get_search_history(15)
            if rows:
                for r in rows:
                    st.info(f"**{r[0].upper()}** | {r[1][:50]} | {str(r[2])[:16]}")
                st.caption(f"Showing {len(rows)} entries")
            else:
                st.write("No searches yet. Start chatting!")

    with h2:
        st.markdown("### 🗺️ Saved Itineraries")
        if st.button("🔄 Load Itineraries", use_container_width=True):
            rows = get_saved_itineraries()
            if rows:
                for r in rows:
                    st.success(
                        f"📍 **{r[0]}** | {r[1]} days | "
                        f"{r[2]} | {r[3]} travelers | {str(r[4])[:10]}"
                    )
                st.caption(f"{len(rows)} itineraries saved")
            else:
                st.write("No itineraries saved yet. Use Trip Planner!")

# ════════════════════════════════════════════════════
# TAB 6 — ABOUT
# ════════════════════════════════════════════════════
with tab6:
    st.subheader("ℹ️ About This Project")
    a1, a2 = st.columns(2)

    with a1:
        st.markdown(f"""
        ## AI Travel Concierge
        **Internship Project | Track A | 8 Weeks**

        ### Tech Stack
        | Component | Technology |
        |-----------|------------|
        | LLM | Groq ({model_name}) |
        | Framework | LangChain |
        | RAG | FAISS + HuggingFace |
        | Database | SQLite |
        | UI | Streamlit |
        | Deployment | Streamlit Cloud |

        ### APIs Used
        | API | Purpose |
        |-----|---------|
        | Groq | AI Language Model |
        | SERP API | Flights, Hotels, Search |
        | Weatherstack | Weather Data |
        | ExchangeRate | Currency Rates |
        """)

    with a2:
        st.markdown("""
        ### Weekly Progress

        **Week 1-2: Foundation & RAG**
        - RAG knowledge base (FAISS + HuggingFace)
        - 7 travel knowledge documents
        - Basic chat interface

        **Week 3-4: Agent + 5 Tools**
        - Weather tool (240+ cities worldwide)
        - Currency converter (live rates + offline fallback)
        - Flight search (SERP API)
        - Hotel search (SERP API)
        - General travel web search

        **Week 5-6: Specialization**
        - Day-wise itinerary generator (LLM-powered)
        - Budget estimator (25+ destinations)
        - SQLite database (auto-saves all searches)

        **Week 7-8: Final Polish**
        - Export trip plans as downloadable .txt
        - Automated test suite (5 tests)
        - Deployed on Streamlit Cloud

        ---
        - ✅ Week 1-2: Foundation & RAG
        - ✅ Week 3-4: Agent + Tools
        - ✅ Week 5-6: Itinerary + Budget + DB
        - ✅ Week 7-8: Final Polish + Deployment
        """)
