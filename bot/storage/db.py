from datetime import datetime, timezone
from typing import TYPE_CHECKING

import aiosqlite

from bot.config import DB_PATH

if TYPE_CHECKING:
    from bot.game.loot import Catch

SCHEMA = """
CREATE TABLE IF NOT EXISTS players (
    user_id INTEGER PRIMARY KEY,
    username TEXT,
    language TEXT,
    coins INTEGER NOT NULL DEFAULT 0,
    cast_location TEXT,
    cast_ready_at REAL,
    created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS catches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    species TEXT NOT NULL,
    rarity TEXT NOT NULL,
    weight REAL NOT NULL,
    coins INTEGER NOT NULL,
    location TEXT NOT NULL,
    caught_at TEXT NOT NULL,
    sold INTEGER NOT NULL DEFAULT 0
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


async def start_cast(user_id: int, location: str, ready_at: float) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE players SET cast_location = ?, cast_ready_at = ? "
            "WHERE user_id = ?",
            (location, ready_at, user_id),
        )
        await conn.commit()


async def clear_cast(user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE players SET cast_location = NULL, cast_ready_at = NULL "
            "WHERE user_id = ?",
            (user_id,),
        )
        await conn.commit()


async def record_catch(
    user_id: int, catch: "Catch", location: str, caught_at: str
) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "INSERT INTO catches "
            "(user_id, species, rarity, weight, coins, location, caught_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                user_id,
                catch.species,
                catch.rarity,
                catch.weight,
                catch.coins,
                location,
                caught_at,
            ),
        )
        await conn.commit()
