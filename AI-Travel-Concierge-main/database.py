# ============================================================
# database.py
# SQLite database — all tables + CRUD helpers
# ============================================================
import sqlite3

DB_PATH = "travel_concierge.db"


def init_database():
    """Create tables if they don't exist. Call once on startup."""
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS search_history (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            search_type TEXT NOT NULL,
            query       TEXT NOT NULL,
            result      TEXT,
            timestamp   TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS itineraries (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            destination    TEXT NOT NULL,
            duration_days  INTEGER,
            budget_level   TEXT,
            travelers      INTEGER DEFAULT 1,
            itinerary_text TEXT,
            estimated_cost TEXT,
            created_at     TEXT DEFAULT (datetime('now'))
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_preferences (
            id             INTEGER PRIMARY KEY AUTOINCREMENT,
            preference_key TEXT UNIQUE,
            preference_val TEXT,
            updated_at     TEXT DEFAULT (datetime('now'))
        )
    """)

    conn.commit()
    conn.close()


# ── Write helpers ─────────────────────────────────────────────

def save_search(search_type: str, query: str, result: str) -> None:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            "INSERT INTO search_history (search_type, query, result) VALUES (?,?,?)",
            (search_type, query[:200], result[:500]),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


def save_itinerary(destination: str, days: int, budget: str,
                   travelers: int, itinerary: str, cost: str) -> None:
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.execute(
            """INSERT INTO itineraries
               (destination, duration_days, budget_level,
                travelers, itinerary_text, estimated_cost)
               VALUES (?,?,?,?,?,?)""",
            (destination, days, budget, travelers, itinerary, cost),
        )
        conn.commit()
        conn.close()
    except Exception:
        pass


# ── Read helpers ──────────────────────────────────────────────

def get_search_history(limit: int = 15) -> list:
    try:
        conn  = sqlite3.connect(DB_PATH)
        rows  = conn.execute(
            "SELECT search_type, query, timestamp FROM search_history "
            "ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
        conn.close()
        return rows
    except Exception:
        return []


def get_saved_itineraries() -> list:
    try:
        conn = sqlite3.connect(DB_PATH)
        rows = conn.execute(
            "SELECT destination, duration_days, budget_level, "
            "travelers, created_at FROM itineraries ORDER BY id DESC"
        ).fetchall()
        conn.close()
        return rows
    except Exception:
        return []
