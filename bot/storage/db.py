from datetime import datetime, timezone

import aiosqlite

from bot.config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS players (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    language TEXT,
    coins INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
"""


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.executescript(SCHEMA)
        await conn.commit()


async def get_or_create_player(user_id: int, username: str | None) -> aiosqlite.Row:
    now = datetime.now(timezone.utc).isoformat()
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        await conn.execute(
            "INSERT OR IGNORE INTO players (user_id, username, created_at) "
            "VALUES (?, ?, ?)",
            (user_id, username, now),
        )
        await conn.commit()
        async with conn.execute(
            "SELECT * FROM players WHERE user_id = ?", (user_id,)
        ) as cursor:
            return await cursor.fetchone()


async def set_language(user_id: int, language: str) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE players SET language = ? WHERE user_id = ?",
            (language, user_id),
        )
        await conn.commit()
