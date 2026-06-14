# fishing-game

Telegram fishing game bot - cast, wait, pull. Inline-button gameplay with
timed catches, rarity rolls, rods, baits, and leaderboards.

## Stack
- aiogram 3.x
- aiosqlite / SQLite
- Long polling (no open ports), Railway-friendly

## Run
1. `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and set `BOT_TOKEN`.
3. `python -m bot.main`
