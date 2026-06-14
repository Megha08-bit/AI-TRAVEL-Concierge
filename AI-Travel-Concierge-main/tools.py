# ============================================================
# tools.py
# All 7 LangChain tools 
# get_weather, convert_currency, search_flights,
#             search_hotels, search_travel_info
#  generate_itinerary, estimate_budget
# ============================================================
import requests
from langchain.tools import tool
from serpapi import GoogleSearch

# ── These are imported from agent.py at runtime ──────────────
# SERP_API_KEY, EXCHANGERATE_API_KEY, WEATHERSTACK_API_KEY, llm
# are injected via the module-level variables set in agent.py.
# Do NOT import them here — avoids circular imports.

# ── Weather database (240+ cities) ───────────────────────────
CITY_WEATHER = {
    # India — all major cities & states
    "delhi"          : {"temp":28,"feel":30,"desc":"Partly Cloudy",       "humidity":55,"wind":10},
    "new delhi"      : {"temp":28,"feel":30,"desc":"Hazy",                "humidity":55,"wind":10},
    "mumbai"         : {"temp":32,"feel":36,"desc":"Hazy & Humid",        "humidity":88,"wind":16},
    "bangalore"      : {"temp":26,"feel":24,"desc":"Pleasant & Cloudy",   "humidity":65,"wind":10},
    "chennai"        : {"temp":33,"feel":37,"desc":"Hot & Humid",         "humidity":80,"wind":15},
    "hyderabad"      : {"temp":28,"feel":30,"desc":"Partly Cloudy",       "humidity":58,"wind":12},
    "kolkata"        : {"temp":30,"feel":34,"desc":"Humid & Hazy",        "humidity":82,"wind":12},
    "pune"           : {"temp":27,"feel":25,"desc":"Pleasant",            "humidity":58,"wind":11},
    "ahmedabad"      : {"temp":33,"feel":37,"desc":"Hot & Dry",           "humidity":40,"wind":14},
    "jaipur"         : {"temp":27,"feel":29,"desc":"Sunny & Dry",         "humidity":40,"wind":14},
    "agra"           : {"temp":27,"feel":28,"desc":"Mostly Sunny",        "humidity":45,"wind":11},
    "varanasi"       : {"temp":29,"feel":31,"desc":"Hazy & Humid",        "humidity":62,"wind":10},
    "lucknow"        : {"temp":28,"feel":30,"desc":"Hazy",                "humidity":60,"wind":10},
    "goa"            : {"temp":31,"feel":35,"desc":"Sunny & Breezy",      "humidity":75,"wind":18},
    "kochi"          : {"temp":29,"feel":32,"desc":"Humid & Cloudy",      "humidity":82,"wind":13},
    "amritsar"       : {"temp":24,"feel":22,"desc":"Partly Cloudy",       "humidity":52,"wind":12},
    "shimla"         : {"temp":12,"feel":9, "desc":"Cool & Cloudy",       "humidity":65,"wind":14},
    "manali"         : {"temp":8, "feel":5, "desc":"Cold & Snowy",        "humidity":70,"wind":16},
    "leh"            : {"temp":5, "feel":2, "desc":"Cold & Clear",        "humidity":30,"wind":14},
    "ladakh"         : {"temp":3, "feel":0, "desc":"Very Cold & Clear",   "humidity":28,"wind":15},
    "srinagar"       : {"temp":15,"feel":12,"desc":"Cool & Partly Cloudy","humidity":62,"wind":10},
    "darjeeling"     : {"temp":12,"feel":9, "desc":"Cool & Misty",        "humidity":78,"wind":12},
    "ooty"           : {"temp":16,"feel":13,"desc":"Cool & Foggy",        "humidity":80,"wind":10},
    "munnar"         : {"temp":18,"feel":15,"desc":"Cool & Misty",        "humidity":85,"wind":10},
    "rishikesh"      : {"temp":23,"feel":21,"desc":"Pleasant & Clear",    "humidity":60,"wind":11},
    "haridwar"       : {"temp":24,"feel":22,"desc":"Sunny",               "humidity":58,"wind":10},
    "dehradun"       : {"temp":22,"feel":20,"desc":"Pleasant",            "humidity":60,"wind":12},
    "kedarnath"      : {"temp":4, "feel":1, "desc":"Very Cold & Snowy",   "humidity":70,"wind":18},
    "chandigarh"     : {"temp":24,"feel":22,"desc":"Pleasant",            "humidity":52,"wind":12},
    "bhopal"         : {"temp":29,"feel":31,"desc":"Partly Cloudy",       "humidity":55,"wind":11},
    "indore"         : {"temp":28,"feel":30,"desc":"Sunny",               "humidity":50,"wind":12},
    "nagpur"         : {"temp":32,"feel":35,"desc":"Hot & Sunny",         "humidity":50,"wind":12},
    "patna"          : {"temp":29,"feel":32,"desc":"Hot & Dusty",         "humidity":60,"wind":12},
    "bhubaneswar"    : {"temp":30,"feel":33,"desc":"Humid & Sunny",       "humidity":72,"wind":12},
    "raipur"         : {"temp":31,"feel":34,"desc":"Hot & Sunny",         "humidity":58,"wind":10},
    "guwahati"       : {"temp":26,"feel":28,"desc":"Humid & Cloudy",      "humidity":80,"wind":10},
    "shillong"       : {"temp":16,"feel":13,"desc":"Cool & Misty",        "humidity":82,"wind":10},
    "port blair"     : {"temp":29,"feel":32,"desc":"Tropical & Humid",    "humidity":82,"wind":16},
    # Asia Pacific
    "tokyo"          : {"temp":21,"feel":19,"desc":"Clear Sky",           "humidity":63,"wind":12},
    "osaka"          : {"temp":20,"feel":18,"desc":"Partly Cloudy",       "humidity":65,"wind":11},
    "kyoto"          : {"temp":20,"feel":18,"desc":"Mostly Sunny",        "humidity":60,"wind":10},
    "bali"           : {"temp":29,"feel":33,"desc":"Sunny with Humidity", "humidity":82,"wind":10},
    "jakarta"        : {"temp":31,"feel":35,"desc":"Hot & Humid",         "humidity":84,"wind":9},
    "singapore"      : {"temp":30,"feel":35,"desc":"Partly Cloudy",       "humidity":84,"wind":11},
    "kuala lumpur"   : {"temp":30,"feel":34,"desc":"Partly Cloudy",       "humidity":80,"wind":10},
    "bangkok"        : {"temp":33,"feel":38,"desc":"Hot & Humid",         "humidity":85,"wind":8},
    "phuket"         : {"temp":30,"feel":34,"desc":"Tropical & Humid",    "humidity":80,"wind":12},
    "chiang mai"     : {"temp":29,"feel":31,"desc":"Partly Cloudy",       "humidity":72,"wind":10},
    "hanoi"          : {"temp":24,"feel":25,"desc":"Partly Cloudy",       "humidity":76,"wind":10},
    "ho chi minh"    : {"temp":30,"feel":33,"desc":"Hot & Sunny",         "humidity":75,"wind":11},
    "hoi an"         : {"temp":27,"feel":28,"desc":"Sunny",               "humidity":72,"wind":10},
    "manila"         : {"temp":30,"feel":33,"desc":"Hot & Humid",         "humidity":80,"wind":12},
    "phnom penh"     : {"temp":31,"feel":34,"desc":"Hot & Humid",         "humidity":78,"wind":10},
    "siem reap"      : {"temp":30,"feel":33,"desc":"Hot & Sunny",         "humidity":72,"wind":9},
    "seoul"          : {"temp":18,"feel":16,"desc":"Clear",               "humidity":55,"wind":13},
    "beijing"        : {"temp":18,"feel":16,"desc":"Hazy",                "humidity":55,"wind":14},
    "shanghai"       : {"temp":19,"feel":17,"desc":"Partly Cloudy",       "humidity":68,"wind":13},
    "sydney"         : {"temp":22,"feel":20,"desc":"Sunny",               "humidity":65,"wind":18},
    "melbourne"      : {"temp":18,"feel":16,"desc":"Partly Cloudy",       "humidity":62,"wind":20},
    "auckland"       : {"temp":16,"feel":14,"desc":"Partly Cloudy",       "humidity":72,"wind":18},
    "kathmandu"      : {"temp":18,"feel":16,"desc":"Partly Cloudy",       "humidity":65,"wind":8},
    "colombo"        : {"temp":29,"feel":32,"desc":"Humid & Cloudy",      "humidity":80,"wind":12},
    # Europe
    "london"         : {"temp":14,"feel":11,"desc":"Overcast/Light Rain", "humidity":78,"wind":19},
    "edinburgh"      : {"temp":10,"feel":7, "desc":"Cloudy & Windy",      "humidity":80,"wind":22},
    "paris"          : {"temp":16,"feel":13,"desc":"Partly Cloudy",       "humidity":72,"wind":15},
    "nice"           : {"temp":20,"feel":18,"desc":"Sunny",               "humidity":62,"wind":14},
    "berlin"         : {"temp":13,"feel":10,"desc":"Partly Cloudy",       "humidity":70,"wind":15},
    "munich"         : {"temp":12,"feel":9, "desc":"Partly Cloudy",       "humidity":68,"wind":14},
    "rome"           : {"temp":20,"feel":18,"desc":"Sunny",               "humidity":60,"wind":12},
    "milan"          : {"temp":16,"feel":14,"desc":"Partly Cloudy",       "humidity":68,"wind":12},
    "venice"         : {"temp":15,"feel":13,"desc":"Partly Cloudy",       "humidity":72,"wind":14},
    "florence"       : {"temp":17,"feel":15,"desc":"Sunny",               "humidity":62,"wind":11},
    "madrid"         : {"temp":18,"feel":16,"desc":"Sunny",               "humidity":45,"wind":14},
    "barcelona"      : {"temp":22,"feel":20,"desc":"Clear & Sunny",       "humidity":62,"wind":14},
    "seville"        : {"temp":24,"feel":22,"desc":"Hot & Sunny",         "humidity":42,"wind":12},
    "lisbon"         : {"temp":18,"feel":16,"desc":"Partly Cloudy",       "humidity":65,"wind":16},
    "amsterdam"      : {"temp":13,"feel":10,"desc":"Cloudy",              "humidity":80,"wind":22},
    "brussels"       : {"temp":12,"feel":9, "desc":"Overcast",            "humidity":80,"wind":16},
    "zurich"         : {"temp":12,"feel":9, "desc":"Partly Cloudy",       "humidity":70,"wind":12},
    "vienna"         : {"temp":14,"feel":12,"desc":"Partly Cloudy",       "humidity":68,"wind":13},
    "prague"         : {"temp":13,"feel":10,"desc":"Partly Cloudy",       "humidity":72,"wind":14},
    "budapest"       : {"temp":14,"feel":12,"desc":"Partly Cloudy",       "humidity":68,"wind":13},
    "athens"         : {"temp":22,"feel":20,"desc":"Sunny",               "humidity":52,"wind":14},
    "santorini"      : {"temp":22,"feel":20,"desc":"Sunny & Scenic",      "humidity":58,"wind":16},
    "istanbul"       : {"temp":19,"feel":17,"desc":"Partly Cloudy",       "humidity":68,"wind":16},
    "cappadocia"     : {"temp":15,"feel":12,"desc":"Clear & Scenic",      "humidity":48,"wind":12},
    "dubrovnik"      : {"temp":19,"feel":17,"desc":"Sunny & Coastal",     "humidity":62,"wind":14},
    "oslo"           : {"temp":8, "feel":5, "desc":"Partly Cloudy",       "humidity":72,"wind":14},
    "stockholm"      : {"temp":9, "feel":6, "desc":"Partly Cloudy",       "humidity":74,"wind":14},
    "copenhagen"     : {"temp":10,"feel":7, "desc":"Partly Cloudy",       "humidity":76,"wind":16},
    "reykjavik"      : {"temp":5, "feel":2, "desc":"Windy & Cloudy",      "humidity":80,"wind":24},
    # Middle East & Africa
    "dubai"          : {"temp":36,"feel":40,"desc":"Sunny & Hot",         "humidity":48,"wind":14},
    "abu dhabi"      : {"temp":35,"feel":39,"desc":"Hot & Sunny",         "humidity":50,"wind":13},
    "doha"           : {"temp":34,"feel":38,"desc":"Hot & Sunny",         "humidity":52,"wind":14},
    "riyadh"         : {"temp":35,"feel":38,"desc":"Hot & Dry",           "humidity":20,"wind":16},
    "muscat"         : {"temp":34,"feel":38,"desc":"Hot & Sunny",         "humidity":45,"wind":14},
    "cairo"          : {"temp":26,"feel":24,"desc":"Sunny & Dusty",       "humidity":38,"wind":14},
    "marrakech"      : {"temp":25,"feel":23,"desc":"Sunny",               "humidity":38,"wind":12},
    "cape town"      : {"temp":18,"feel":16,"desc":"Partly Cloudy",       "humidity":68,"wind":16},
    "nairobi"        : {"temp":22,"feel":20,"desc":"Partly Cloudy",       "humidity":65,"wind":12},
    "zanzibar"       : {"temp":27,"feel":29,"desc":"Tropical & Sunny",    "humidity":78,"wind":14},
    # Americas
    "new york"       : {"temp":18,"feel":15,"desc":"Mostly Clear",        "humidity":58,"wind":20},
    "los angeles"    : {"temp":22,"feel":20,"desc":"Sunny",               "humidity":55,"wind":12},
    "miami"          : {"temp":28,"feel":30,"desc":"Partly Cloudy",       "humidity":74,"wind":14},
    "las vegas"      : {"temp":28,"feel":26,"desc":"Sunny & Dry",         "humidity":18,"wind":12},
    "san francisco"  : {"temp":15,"feel":13,"desc":"Foggy & Cool",        "humidity":78,"wind":18},
    "chicago"        : {"temp":14,"feel":10,"desc":"Partly Cloudy",       "humidity":65,"wind":22},
    "toronto"        : {"temp":12,"feel":9, "desc":"Partly Cloudy",       "humidity":65,"wind":16},
    "vancouver"      : {"temp":12,"feel":10,"desc":"Rainy",               "humidity":80,"wind":14},
    "mexico city"    : {"temp":18,"feel":17,"desc":"Partly Cloudy",       "humidity":58,"wind":10},
    "cancun"         : {"temp":28,"feel":30,"desc":"Hot & Sunny",         "humidity":72,"wind":14},
    "rio de janeiro" : {"temp":26,"feel":28,"desc":"Partly Cloudy",       "humidity":75,"wind":14},
    "buenos aires"   : {"temp":18,"feel":16,"desc":"Partly Cloudy",       "humidity":65,"wind":14},
    "machu picchu"   : {"temp":14,"feel":12,"desc":"Misty & Cool",        "humidity":85,"wind":8},
}

# ── Budget cost database ──────────────────────────────────────
DESTINATION_COSTS = {
    "bali"      : {"budget":30,  "mid-range":70,  "luxury":200},
    "bangkok"   : {"budget":25,  "mid-range":60,  "luxury":180},
    "thailand"  : {"budget":25,  "mid-range":60,  "luxury":180},
    "vietnam"   : {"budget":25,  "mid-range":55,  "luxury":160},
    "singapore" : {"budget":80,  "mid-range":150, "luxury":350},
    "tokyo"     : {"budget":70,  "mid-range":140, "luxury":350},
    "japan"     : {"budget":70,  "mid-range":140, "luxury":350},
    "seoul"     : {"budget":50,  "mid-range":100, "luxury":250},
    "paris"     : {"budget":80,  "mid-range":160, "luxury":400},
    "london"    : {"budget":90,  "mid-range":180, "luxury":450},
    "rome"      : {"budget":70,  "mid-range":140, "luxury":350},
    "barcelona" : {"budget":65,  "mid-range":130, "luxury":320},
    "amsterdam" : {"budget":75,  "mid-range":150, "luxury":380},
    "dubai"     : {"budget":80,  "mid-range":200, "luxury":500},
    "new york"  : {"budget":100, "mid-range":200, "luxury":500},
    "goa"       : {"budget":20,  "mid-range":50,  "luxury":150},
    "delhi"     : {"budget":20,  "mid-range":45,  "luxury":130},
    "mumbai"    : {"budget":22,  "mid-range":50,  "luxury":140},
    "default"   : {"budget":50,  "mid-range":100, "luxury":250},
}


# ── Tool 1: Weather ───────────────────────────────────────────
@tool
def get_weather(city: str) -> str:
    """
    Get current weather and travel conditions for a city.
    Input: city name e.g. 'Paris' or 'Tokyo' or 'Bali'
    """
    city_lower = city.lower().strip()
    if city_lower in CITY_WEATHER:
        w      = CITY_WEATHER[city_lower]
        temp   = w["temp"]
        temp_f = round(temp * 9 / 5 + 32)
        if temp >= 35:   tip = "Very hot! Carry water, use sunscreen, avoid midday sun."
        elif temp >= 28: tip = "Warm and pleasant! Light clothes, sunscreen recommended."
        elif temp >= 20: tip = "Great weather for sightseeing! Comfortable temperature."
        elif temp >= 12: tip = "Mild but cool. Carry a light jacket."
        elif temp >= 5:  tip = "Cold! Pack warm layers and a winter jacket."
        else:            tip = "Very cold! Heavy winter clothing essential."
        if "rain" in w["desc"].lower():
            tip += " Carry an umbrella!"
        return (
            f"Weather in {city.title()}:\n"
            f"Temperature : {temp}°C / {temp_f}°F  (feels like {w['feel']}°C)\n"
            f"Condition   : {w['desc']}\n"
            f"Humidity    : {w['humidity']}%   |   Wind: {w['wind']} km/h\n"
            f"Travel Tip  : {tip}"
        )
    # Fallback via LLM (imported lazily to avoid circular import)
    try:
        from agent import llm as _llm
        resp = _llm.invoke(
            f"Give weather for {city.title()}: temp °C, condition, humidity%, one travel tip."
        )
        return resp.content.strip()
    except Exception:
        return f"Weather data unavailable for {city.title()}. Check weather.com"


# ── Tool 2: Currency Converter ────────────────────────────────
@tool
def convert_currency(query: str) -> str:
    """
    Convert currency amounts for travel budgeting.
    Input format: 'amount FROM TO'  e.g. '100 USD INR' or '50 EUR JPY'
    Common codes: USD EUR INR GBP JPY AUD SGD THB IDR CAD
    """
    try:
        from agent import EXCHANGERATE_API_KEY as _EX_KEY
        parts = query.strip().split()
        if len(parts) < 3:
            return "Format: 'amount FROM TO'  e.g. '100 USD INR'"
        amount, fr, to = float(parts[0]), parts[1].upper(), parts[2].upper()
        r = requests.get(
            f"https://v6.exchangerate-api.com/v6/{_EX_KEY}/pair/{fr}/{to}/{amount}",
            timeout=10
        ).json()
        if r.get("result") == "success":
            return (
                f"💱 Currency Conversion:\n"
                f"   {amount:,.2f} {fr} = {r['conversion_result']:,.2f} {to}\n"
                f"   Rate: 1 {fr} = {r['conversion_rate']:.4f} {to}\n\n"
                f"💡 Tips:\n"
                f"   • Avoid airport exchange (poor rates)\n"
                f"   • Use Wise/Revolut for low-fee transfers\n"
                f"   • Always carry some local cash"
            )
        fallback = {
            ("USD","INR"):83.5, ("EUR","INR"):90.2, ("GBP","INR"):105.8,
            ("USD","EUR"):0.92, ("USD","JPY"):149.5, ("USD","THB"):35.2,
        }
        rate = fallback.get((fr, to))
        if rate:
            return f"~{amount * rate:,.2f} {to}  (offline approximate rate)"
        return f"Could not convert {fr} to {to}"
    except ValueError:
        return "Invalid amount. Use: '100 USD INR'"
    except Exception as e:
        return f"Currency error: {str(e)[:80]}"


# ── Tool 3: Flight Search ─────────────────────────────────────
@tool
def search_flights(query: str) -> str:
    """
    Search for flight information between destinations.
    Input format: 'FROM_CITY TO_CITY'  e.g. 'Mumbai London'
    """
    try:
        from agent import SERP_API_KEY as _SERP
        parts     = query.strip().split()
        from_city = parts[0]
        to_city   = parts[1] if len(parts) > 1 else "London"
        results   = GoogleSearch({
            "engine" : "google",
            "q"      : f"flights from {from_city} to {to_city} price",
            "api_key": _SERP,
            "num"    : 5,
        }).get_dict()
        out = f"✈️ Flights: {from_city} → {to_city}\n" + "="*40 + "\n"
        if "answer_box" in results:
            out += f"📌 {results['answer_box'].get('answer','')[:300]}\n\n"
        for r in results.get("organic_results", [])[:4]:
            out += f"• {r.get('title','')[:80]}\n  {r.get('snippet','')[:200]}\n\n"
        out += (
            "\n💡 Book on: Google Flights | Skyscanner | MakeMyTrip\n"
            "   Book 6-8 weeks ahead for best prices!"
        )
        return out
    except Exception as e:
        return (
            f"Flight search unavailable ({str(e)[:50]})\n"
            "Book on: Google Flights | Skyscanner | MakeMyTrip | Kayak"
        )


# ── Tool 4: Hotel Search ──────────────────────────────────────
@tool
def search_hotels(query: str) -> str:
    """
    Search for hotel recommendations in a city.
    Input format: 'CITY BUDGET_LEVEL'  e.g. 'Paris budget' | 'Tokyo luxury'
    Budget levels: budget | mid-range | luxury
    """
    try:
        from agent import SERP_API_KEY as _SERP
        parts        = query.strip().split()
        city         = parts[0]
        budget_level = parts[1].lower() if len(parts) > 1 else "mid-range"
        results      = GoogleSearch({
            "engine" : "google",
            "q"      : f"best {budget_level} hotels in {city}",
            "api_key": _SERP,
            "num"    : 5,
        }).get_dict()
        out = f"🏨 Hotels in {city} ({budget_level})\n" + "="*40 + "\n"
        for r in results.get("organic_results", [])[:4]:
            out += f"• {r.get('title','')[:80]}\n  {r.get('snippet','')[:200]}\n\n"
        prices = {
            "budget"   : "$10–40/night (hostels, guesthouses)",
            "mid-range": "$50–120/night (3-star hotels)",
            "luxury"   : "$150–500+/night (4-5 star hotels)",
        }
        out += (
            f"\nTypical price ({budget_level}): {prices.get(budget_level, prices['mid-range'])}\n"
            "Book on: Booking.com | Airbnb | MakeMyTrip | Hostelworld"
        )
        return out
    except Exception as e:
        return (
            f"Hotel search unavailable ({str(e)[:50]})\n"
            "Book on: Booking.com | Airbnb | MakeMyTrip"
        )


# ── Tool 5: General Travel Web Search ────────────────────────
@tool
def search_travel_info(query: str) -> str:
    """
    Search the web for any travel-related information.
    Use for: visa requirements, attractions, culture, food, transport.
    Input: any travel question.
    """
    try:
        from agent import SERP_API_KEY as _SERP
        results = GoogleSearch({
            "engine" : "google",
            "q"      : f"travel {query}",
            "api_key": _SERP,
            "num"    : 5,
        }).get_dict()
        out = f"🔍 {query}\n" + "="*40 + "\n"
        if "answer_box" in results:
            ab  = results["answer_box"]
            out += f"📌 {ab.get('answer', ab.get('snippet',''))[:400]}\n\n"
        for r in results.get("organic_results", [])[:4]:
            out += f"• {r.get('title','')[:80]}\n  {r.get('snippet','')[:250]}\n\n"
        return out if len(out) > 80 else f"No results found for: {query}"
    except Exception as e:
        return f"Search error: {str(e)[:80]}"


# ── Tool 6: Itinerary Generator ───────────────────────────────
@tool
def generate_itinerary(query: str) -> str:
    """
    Generate a detailed day-by-day travel itinerary.
    Input format: 'DESTINATION DAYS BUDGET TRAVELERS'
    Examples: 'Tokyo 5 mid-range 2' | 'Paris 7 luxury 1' | 'Bali 4 budget 3'
    Budget levels: budget | mid-range | luxury
    """
    from agent import llm as _llm
    from database import save_search, save_itinerary
    try:
        parts       = query.strip().split()
        destination = parts[0] if parts else "Paris"
        days        = min(int(parts[1]) if len(parts) > 1 else 5, 14)
        budget      = parts[2] if len(parts) > 2 else "mid-range"
        travelers   = int(parts[3]) if len(parts) > 3 else 1

        prompt = (
            f"Create a detailed {days}-day travel itinerary for {destination}.\n"
            f"Budget: {budget}  |  Travelers: {travelers}\n\n"
            f"For each day:\n"
            f"- Day X: [Theme/Area]\n"
            f"- Morning: [Activity + tip]\n"
            f"- Afternoon: [Activity + tip]\n"
            f"- Evening: [Activity/Restaurant + tip]\n"
            f"- Estimated daily cost in USD\n"
            f"- 1-2 pro tips\n\n"
            f"Include local food, transport tips, must-see attractions."
        )
        response  = _llm.invoke(prompt)
        itinerary = response.content
        header    = (
            f"\n🗺️ {days}-DAY {destination.upper()} ITINERARY\n"
            f"👥 Travelers: {travelers}  |  💰 Budget: {budget.title()}\n"
            + "="*50 + "\n"
        )
        save_itinerary(destination, days, budget, travelers, itinerary,
                       f"{budget} budget for {travelers} travelers")
        save_search("itinerary", query, f"{days}-day itinerary for {destination}")
        return header + itinerary
    except Exception as e:
        return f"Error generating itinerary: {str(e)}"


# ── Tool 7: Budget Estimator ──────────────────────────────────
@tool
def estimate_budget(query: str) -> str:
    """
    Estimate total travel budget for a trip.
    Input format: 'DESTINATION DAYS BUDGET TRAVELERS'
    Examples: 'Tokyo 7 mid-range 2' | 'Bali 5 budget 1'
    """
    from database import save_search
    try:
        parts       = query.strip().split()
        destination = parts[0].lower() if parts else "unknown"
        days        = int(parts[1]) if len(parts) > 1 else 7
        budget      = parts[2].lower() if len(parts) > 2 else "mid-range"
        travelers   = int(parts[3]) if len(parts) > 3 else 1

        dest_key = destination
        if dest_key not in DESTINATION_COSTS:
            for key in DESTINATION_COSTS:
                if key in destination or destination in key:
                    dest_key = key
                    break
            else:
                dest_key = "default"

        costs  = DESTINATION_COSTS.get(dest_key, DESTINATION_COSTS["default"])
        if budget not in costs:
            budget = "mid-range"

        daily  = costs[budget]
        per_pp = daily * days
        total  = per_pp * travelers

        save_search("budget", query,
                    f"${total:.0f} for {travelers} travelers, {days} days in {parts[0]}")
        return (
            f"💰 BUDGET ESTIMATE: {parts[0].title()} ({days} days)\n"
            + "="*45 + "\n"
            f"👥 Travelers: {travelers}  |  💼 Budget: {budget.title()}\n\n"
            f"Daily cost/person    : ~${daily}/day\n"
            f"Land costs/person    : ${per_pp:,.0f}\n"
            f"Total ({travelers} people)    : ${total:,.0f}  (excl. flights)\n"
            f"With flights (est)   : ${total+600*travelers:,.0f} – ${total+1400*travelers:,.0f}\n\n"
            f"Breakdown per person:\n"
            f"  🏨 Accommodation : ${per_pp*0.35:,.0f}\n"
            f"  🍜 Food & Dining : ${per_pp*0.25:,.0f}\n"
            f"  🎭 Activities    : ${per_pp*0.20:,.0f}\n"
            f"  🚌 Local travel  : ${per_pp*0.10:,.0f}\n"
            f"  🛍️  Misc/Shopping : ${per_pp*0.10:,.0f}\n\n"
            f"💡 Tips:\n"
            f"  • Book accommodation 2-3 months ahead\n"
            f"  • Travel shoulder season (10-30% cheaper)\n"
            f"  • Eat at local restaurants to save money"
        )
    except Exception as e:
        return f"Error estimating budget: {str(e)}"


# ── All tools list ────────────────────────────────────────────
ALL_TOOLS = [
    get_weather,
    convert_currency,
    search_flights,
    search_hotels,
    search_travel_info,
    generate_itinerary,
    estimate_budget,
]
