import logging
import os
from dotenv import load_dotenv
from bot.runner import run_once

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    # Local dev uses .env; on Render, env vars come from the dashboard.
    load_dotenv()

    token = os.getenv("STRATZ_TOKEN", "").strip()
    if not token:
        logging.error("STRATZ_TOKEN is not set. Add it to .env (local) or Render env vars.")
        raise SystemExit(2)

    ok = run_once(token)
    raise SystemExit(0 if ok else 1)
