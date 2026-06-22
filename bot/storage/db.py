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
    cast_notified INTEGER NOT NULL DEFAULT 0,
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


async def _column_exists(conn: aiosqlite.Connection, table: str, column: str) -> bool:
    async with conn.execute(f"PRAGMA table_info({table})") as cursor:
        return any(row[1] == column for row in await cursor.fetchall())


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.executescript(SCHEMA)
        if not await _column_exists(conn, "players", "cast_notified"):
            await conn.execute(
                "ALTER TABLE players "
                "ADD COLUMN cast_notified INTEGER NOT NULL DEFAULT 0"
            )
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
            "UPDATE players "
            "SET cast_location = ?, cast_ready_at = ?, cast_notified = 0 "
            "WHERE user_id = ?",
            (location, ready_at, user_id),
        )
        await conn.commit()


async def clear_cast(user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE players "
            "SET cast_location = NULL, cast_ready_at = NULL, cast_notified = 0 "
            "WHERE user_id = ?",
            (user_id,),
        )
        await conn.commit()


async def claim_cast(user_id: int, now: float) -> bool:
    async with aiosqlite.connect(DB_PATH) as conn:
        cursor = await conn.execute(
            "UPDATE players "
            "SET cast_location = NULL, cast_ready_at = NULL, cast_notified = 0 "
            "WHERE user_id = ? AND cast_ready_at IS NOT NULL AND cast_ready_at <= ?",
            (user_id, now),
        )
        await conn.commit()
        return cursor.rowcount == 1


async def due_casts(now: float) -> list[aiosqlite.Row]:
    async with aiosqlite.connect(DB_PATH) as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute(
            "SELECT user_id, language FROM players "
            "WHERE cast_ready_at IS NOT NULL AND cast_ready_at <= ? "
            "AND cast_notified = 0",
            (now,),
        ) as cursor:
            return await cursor.fetchall()


async def mark_notified(user_id: int) -> None:
    async with aiosqlite.connect(DB_PATH) as conn:
        await conn.execute(
            "UPDATE players SET cast_notified = 1 WHERE user_id = ?",
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
