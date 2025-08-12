import logging
from bot.config import load_config
from bot.fetch import get_latest_for_player

def _summarize_line(match: dict, my_steam32: int) -> str:
    me = next((p for p in match.get("players", []) if p.get("steamAccountId") == my_steam32), None)
    if not me:
        return f"match {match.get('id')} fetched, but player {my_steam32} not in players[]"

    hero = (me.get("hero", {}) or {}).get("displayName") or (me.get("hero", {}) or {}).get("name") or "Unknown Hero"
    k = me.get("kills", 0); d = me.get("deaths", 0); a = me.get("assists", 0)
    imp = me.get("imp", 0)
    wl = "Win" if me.get("isVictory") else "Loss"
    dur = match.get("durationSeconds", 0)
    return f"OK: match {match.get('id')} • {wl} • {dur//60}:{dur%60:02d} • {k}/{d}/{a} on {hero} • IMP {imp}"

def run_once(token: str) -> bool:
    cfg = load_config()
    steam32 = int(cfg["steam32_id"])
    bundle = get_latest_for_player(steam32, token)
    if not bundle:
        logging.info("No data returned.")
        return False

    line = _summarize_line(bundle["match"], steam32)
    logging.info(line)
    return True
