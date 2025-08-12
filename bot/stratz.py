import logging
import os
import requests
from bot.throttle import throttle

STRATZ_URL = "https://api.stratz.com/graphql"

def _post(query: str, variables: dict, token: str = None, timeout: int = 15):
    """
    Internal helper to send a POST request to the Stratz API.
    Falls back to reading STRATZ_TOKEN from the environment if no token is passed.
    """
    if not token:
        token = os.getenv("STRATZ_TOKEN", "").strip()

    headers = {
        "User-Agent": "STRATZ_API",  # per your request
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }

    throttle()
    resp = requests.post(
        STRATZ_URL,
        headers=headers,
        json={"query": query, "variables": variables},
        timeout=timeout,
    )

    if resp.status_code == 429:
        logging.warning("Stratz 429 Too Many Requests")
        return "quota_exceeded"

    try:
        resp.raise_for_status()
    except requests.HTTPError:
        logging.error("HTTP %s from Stratz: %s", resp.status_code, resp.text[:400])
        return None

    payload = resp.json()
    if "errors" in payload and payload["errors"]:
        logging.error("GraphQL errors: %s", payload["errors"])
        return None
    return payload.get("data")

def fetch_latest_match_id(steam32_id: int, token: str = None):
    """
    Returns latest match id, or 'quota_exceeded', or None on failure.
    """
    q = """
    query ($steamId: Long!) {
      player(steamAccountId: $steamId) {
        matches(request: { take: 1 }) { id }
      }
    }
    """
    data = _post(q, {"steamId": steam32_id}, token)
    if data == "quota_exceeded":
        return "quota_exceeded"
    if not data or not data.get("player") or not data["player"].get("matches"):
        return None
    return data["player"]["matches"][0]["id"]

def fetch_full_match(match_id: int, token: str = None):
    """
    Returns full match dict (subset of fields), 'quota_exceeded', or None.
    """
    q = """
    query ($matchId: Long!) {
      match(id: $matchId) {
        id
        durationSeconds
        gameMode
        startDateTime
        players {
          steamAccountId
          isRadiant
          isVictory
          lane
          roleBasic
          kills
          deaths
          assists
          imp
          level
          hero { id name displayName }
        }
      }
    }
    """
    data = _post(q, {"matchId": match_id}, token, timeout=18)
    if data == "quota_exceeded":
        return "quota_exceeded"
    if not data or not data.get("match"):
        return None
    return data["match"]
