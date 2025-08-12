import logging
from bot.stratz import fetch_latest_match_id, fetch_full_match

def get_latest_for_player(steam32_id: int, token: str):
    """
    Fetch latest match id and then its full payload.
    Returns dict: {"match_id": int, "match": {...}} or None.
    """
    match_id = fetch_latest_match_id(steam32_id, token)
    if match_id == "quota_exceeded":
        logging.warning("Quota exceeded while getting latest match id.")
        return None
    if match_id is None:
        logging.info("No matches found for player %s.", steam32_id)
        return None

    m = fetch_full_match(match_id, token)
    if m == "quota_exceeded":
        logging.warning("Quota exceeded while getting full match %s.", match_id)
        return None
    if not m:
        logging.error("Failed to fetch full match %s.", match_id)
        return None

    return {"match_id": match_id, "match": m}
