# app/services/bot_classifier.py

from functools import lru_cache

# IMPORT YOUR USER_AGENTS DICT (you already defined it)
from app.data.agents import USER_AGENTS


# -------------------------
# Build fast lookup tables
# -------------------------

# Flatten all substrings into a mapping:
# "googlebot" → "Google"
# "bingbot"   → "Bing"
PATTERN_MAP = {}

for vendor, patterns in USER_AGENTS.items():
    for p in patterns:
        PATTERN_MAP[p.lower()] = vendor


# -------------------------
# Core classifier
# -------------------------


@lru_cache(maxsize=5000)
def identify_bot(user_agent: str) -> str | None:
    """
    Returns:
        - Vendor name (e.g., "Google", "OpenAI", "Perplexity", etc.)
        - None if not a known bot/crawler/AI agent
    """

    if not user_agent:
        return None

    ua = user_agent.lower()

    # Fast substring matching
    for pattern, vendor in PATTERN_MAP.items():
        if pattern in ua:
            return vendor

    return None


# -------------------------
# Summary evaluator
# -------------------------


@lru_cache(maxsize=5000)
def is_bot(user_agent: str) -> bool:
    """True if UA matches any known bot."""
    return identify_bot(user_agent) is not None


# -------------------------
# Categorizer for analytics
# -------------------------


@lru_cache(maxsize=5000)
def classify_user_agent(user_agent: str) -> dict:
    """
    Returns a structured description:
    {
        "is_bot": True/False,
        "vendor": "Google",
        "raw_user_agent": "...",
    }
    """
    vendor = identify_bot(user_agent)

    return {
        "raw_user_agent": user_agent,
        "is_bot": vendor is not None,
        "vendor": vendor,
    }
