"""
Caching utilities for MediGuide AI.

The assignment requires both:

1. InMemoryCache
2. SQLiteCache

LangChain automatically checks the registered cache before making
an LLM request.
"""

from pathlib import Path

from langchain_community.cache import InMemoryCache, SQLiteCache
from langchain_core.globals import set_llm_cache


# Store the SQLite database in the project root
BASE_DIR = Path(__file__).resolve().parent.parent
CACHE_DATABASE = BASE_DIR / "medical_ai_cache.db"


def enable_memory_cache():
    """
    Enable an in-memory LangChain cache.

    Advantages:
        - Very fast
        - Simple
        - Good for one application session

    Disadvantage:
        - Cache disappears when the application stops.
    """

    cache = InMemoryCache()
    set_llm_cache(cache)

    return cache


def enable_sqlite_cache():
    """
    Enable a persistent SQLite LangChain cache.

    Advantages:
        - Persists after application restart
        - Useful for repeated requests across sessions

    Disadvantage:
        - Slightly slower than RAM.
    """

    cache = SQLiteCache(
        database_path=str(CACHE_DATABASE)
    )

    set_llm_cache(cache)

    return cache


def disable_cache():
    """
    Disable LangChain caching.
    """

    set_llm_cache(None)


def configure_cache(cache_type):
    """
    Select the cache used by the application.

    Parameters
    ----------
    cache_type : str
        "In-memory"
        "SQLite"
        "None"

    Returns
    -------
    Cache object or None
    """

    if cache_type == "In-memory":
        return enable_memory_cache()

    elif cache_type == "SQLite":
        return enable_sqlite_cache()

    elif cache_type == "None":
        disable_cache()
        return None

    else:
        raise ValueError(
            f"Unsupported cache type: {cache_type}"
        )


def get_cache_description(cache_type):
    """
    Return a short explanation for the Streamlit UI.
    """

    descriptions = {
        "In-memory": (
            "Fast RAM-based cache. "
            "Cache is lost when the app restarts."
        ),
        "SQLite": (
            "Persistent disk-based cache. "
            "Cache survives application restarts."
        ),
        "None": (
            "Caching is disabled. "
            "Every request is sent to the model."
        ),
    }

    return descriptions.get(
        cache_type,
        "Unknown cache configuration."
    )
