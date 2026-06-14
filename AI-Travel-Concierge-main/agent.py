# ============================================================
# agent.py
# LLM initialisation + TravelAgentExecutor
# Matches the existing agent.py folder in your GitHub repo
# ============================================================
import os
import requests
import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage

# ── API Keys ──────────────────────────────────────────────────
def _get(key: str) -> str:
    try:
        return st.secrets[key]
    except Exception:
        return os.getenv(key, "")

GROQ_API_KEY         = _get("GROQ_API_KEY")
SERP_API_KEY         = _get("SERP_API_KEY")
WEATHERSTACK_API_KEY = _get("WEATHERSTACK_API_KEY")
EXCHANGERATE_API_KEY = _get("EXCHANGERATE_API_KEY")

os.environ["SERPAPI_API_KEY"] = SERP_API_KEY

# ── LLM: load_llm() ──────────────────────────────────────────
GROQ_MODELS = [
    "llama-3.3-70b-versatile",
    "llama-3.1-70b-versatile",
    "llama-3.1-8b-instant",
    "mixtral-8x7b-32768",
    "gemma2-9b-it",
]

llm = None          # module-level so tools.py can import it
_model_name = None

def load_llm():
    """Try each Groq model in order; return (llm, model_name)."""
    global llm, _model_name
    for model in GROQ_MODELS:
        try:
            candidate = ChatGroq(model=model, temperature=0.7, groq_api_key=GROQ_API_KEY)
            candidate.invoke("Hi")
            llm          = candidate
            _model_name  = model
            return llm, model
        except Exception as e:
            print(f"❌ {model}: {str(e)[:50]}")
    return None, None


def get_model_name() -> str:
    return _model_name or "unknown"


# ── Agent logic ───────────────────────────────────────────────
def ask_agent(question: str, tool_map: dict, llm_with_tools) -> str:
    """
    Smart travel agent — tool binding + forced final answer.
    Called by TravelAgentExecutor.invoke().
    """
    from database import save_search

    messages = [
        SystemMessage(content=(
            "You are TravelBot, an expert AI Travel Concierge. "
            "Use tools to get real data. "
            "IMPORTANT: Call only ONE tool at a time."
        )),
        HumanMessage(content=question),
    ]
    try:
        response = llm_with_tools.invoke(messages)

        if not hasattr(response, "tool_calls") or not response.tool_calls:
            save_search("chat", question, response.content[:200])
            return response.content

        messages.append(response)
        all_results = []

        for tc in response.tool_calls:
            name    = tc.get("name", "")
            args    = tc.get("args", {})
            call_id = tc.get("id", "tool_1")
            iv      = list(args.values())[0] if isinstance(args, dict) and args else str(args)
            try:
                result = (
                    tool_map[name].invoke(str(iv))
                    if name in tool_map
                    else f"Tool '{name}' not found"
                )
            except Exception as e:
                result = f"Tool error: {str(e)[:100]}"

            all_results.append(f"[{name}]:\n{result}")
            messages.append(ToolMessage(content=str(result), tool_call_id=call_id))

        combined = "\n\n".join(all_results)
        final    = llm.invoke(
            f"You are TravelBot. Answer: '{question}'\n\n"
            f"Real data from tools:\n{combined}\n\n"
            f"Use ALL data. Be specific with numbers/prices. "
            f"Add 2-3 practical tips. Be friendly and complete."
        )
        save_search("chat", question, final.content[:200])
        return final.content

    except Exception as e:
        err = str(e)
        if "tool_use_failed" in err or "Failed to call" in err:
            try:
                return llm.invoke(
                    f"As travel expert answer: {question}\n"
                    f"Be specific with practical tips and costs."
                ).content
            except Exception as e2:
                return f"Error: {str(e2)[:100]}"
        return f"Error: {err[:150]}"


class TravelAgentExecutor:
    """
    Keeps the same .invoke() interface used throughout the notebook.
    Pass in tools from tools.py after calling load_llm().
    """
    def __init__(self, tool_map: dict, llm_with_tools):
        self.tool_map       = tool_map
        self.llm_with_tools = llm_with_tools

    def invoke(self, inputs: dict) -> dict:
        return {"output": ask_agent(
            inputs.get("input", ""),
            self.tool_map,
            self.llm_with_tools,
        )}


def build_executor(tools_list: list):
    """Helper: bind tools to LLM and return (executor, tool_map)."""
    tool_map       = {t.name: t for t in tools_list}
    llm_with_tools = llm.bind_tools(tools_list)
    executor       = TravelAgentExecutor(tool_map, llm_with_tools)
    return executor, tool_map
