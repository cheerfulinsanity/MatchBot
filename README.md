# GuildBot Minimal (v0.1)
Fetch latest Stratz match for one Steam32 ID and log a single confirmation line. Render-ready worker.

## Quick start (local)
1. `python -m venv .venv && . .venv/bin/activate` (Windows: `.venv\Scripts\activate`)
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and fill STRATZ_TOKEN
4. Set your Steam32 ID in `data/config.json`
5. `python main.py`

Expected log (shape only):
