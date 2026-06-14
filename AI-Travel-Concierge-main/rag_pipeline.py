# ============================================================
# rag_pipeline.py
# RAG knowledge base — FAISS + HuggingFace embeddings
# ============================================================
from langchain_core.documents        import Document
from langchain_text_splitters        import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface           import HuggingFaceEmbeddings
from langchain_core.prompts          import PromptTemplate
from langchain_core.output_parsers   import StrOutputParser
from langchain_core.runnables        import RunnablePassthrough

# ── Travel knowledge documents ────────────────────────────────
TRAVEL_KNOWLEDGE = [
    """
    VISA INFORMATION:
    Most countries require a valid passport with at least 6 months validity.
    Schengen visa covers 26 European countries with a single visa.
    USA requires ESTA for visa-waiver countries or a B1/B2 visa.
    India e-Visa is available for 170+ countries online.
    Always apply for visas 4-6 weeks in advance.
    """,
    """
    TRAVEL BUDGET TIPS:
    Southeast Asia (Thailand, Vietnam, Bali): $30-60/day including accommodation.
    Western Europe averages $100-200/day for mid-range travel.
    Japan costs $80-150/day; best visited in spring (cherry blossoms) or autumn.
    Book flights 6-8 weeks in advance for best prices.
    Use incognito mode when searching flights to avoid price tracking.
    """,
    """
    PACKING ESSENTIALS:
    Always carry: passport, travel insurance docs, emergency cash.
    Universal power adapter for international travel.
    Download offline maps (Google Maps) before arriving.
    Carry copies of all important documents separately.
    Travel insurance is strongly recommended for all trips.
    """,
    """
    TOP DESTINATIONS 2024:
    Europe: Paris, Rome, Barcelona, Amsterdam, Prague
    Asia: Tokyo, Bali, Bangkok, Singapore, Kyoto
    Americas: New York, Machu Picchu, Patagonia, Costa Rica
    Middle East: Dubai, Petra, Istanbul, Muscat
    Best time to visit Bali: April-October (dry season)
    Best time to visit Europe: May-September
    """,
    """
    INDIA TRAVEL INFORMATION:
    North India Golden Triangle (Delhi, Agra, Jaipur): October-March is ideal.
    Kerala backwaters: November-February is best.
    Goa beaches: November-February (peak season), avoid monsoon June-September.
    Himachal Pradesh and Ladakh: May-September.
    Budget: Rs.2000-5000/day for mid-range domestic travel.
    Book trains on IRCTC at least 2-3 months in advance.
    """,
    """
    FLIGHT BOOKING TIPS:
    Best days to book: Tuesday and Wednesday for cheaper fares.
    Use Google Flights, Skyscanner, or Kayak to compare prices.
    Flexible date search can save 20-40% on airfare.
    Budget airlines: IndiGo, SpiceJet (India), Ryanair (Europe), AirAsia (Asia).
    Always check baggage allowance before booking.
    """,
    """
    HOTEL BOOKING TIPS:
    Book directly with hotels for better rates and flexibility.
    Compare on Booking.com, Airbnb, Hotels.com, MakeMyTrip.
    Hostels are great for solo travelers ($10-25/night).
    Mid-range hotels: $40-100/night globally.
    Location matters — staying central saves on transport costs.
    """,
]

# ── RAG prompt ────────────────────────────────────────────────
TRAVEL_PROMPT = PromptTemplate(
    template="""
You are an expert AI Travel Concierge with deep knowledge about travel worldwide.
You are friendly, helpful, and provide practical, actionable travel advice.

Use the following travel knowledge to answer the question:
{context}

Question: {question}

Instructions:
- Be specific and helpful
- Include practical tips when relevant
- Mention costs/budgets when relevant
- If you don't know something specific, say so and give general advice
- Keep response concise but complete

Answer:
""",
    input_variables=["context", "question"],
)


def build_rag_chain(llm):
    """
    Build FAISS vectorstore from travel knowledge,
    return a runnable RAG chain.
    """
    docs       = [Document(page_content=t) for t in TRAVEL_KNOWLEDGE]
    splitter   = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    split_docs = splitter.split_documents(docs)

    embeddings  = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={"device": "cpu"},
        encode_kwargs={"normalize_embeddings": True},
    )
    vectorstore = FAISS.from_documents(split_docs, embeddings)
    retriever   = vectorstore.as_retriever(search_kwargs={"k": 3})

    def _fmt(docs):
        return "\n\n".join(d.page_content for d in docs)

    chain = (
        {"context": retriever | _fmt, "question": RunnablePassthrough()}
        | TRAVEL_PROMPT
        | llm
        | StrOutputParser()
    )
    return chain


def rag_chat(question: str, chain) -> str:
    """Ask the RAG chain a question."""
    try:
        return chain.invoke(question)
    except Exception as e:
        return f"RAG error: {str(e)}"
