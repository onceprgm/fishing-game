from datetime import datetime, timezone

import aiosqlite
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from bot import i18n
from bot.game import loot
from bot.game.locations import LOCATIONS
from bot.keyboards import main_menu_keyboard, waiting_keyboard
from bot.storage import db

router = Router()


def _language(player: aiosqlite.Row) -> str:
    return player["language"] or i18n.DEFAULT_LANGUAGE


@router.callback_query(F.data.startswith("cast:"))
async def handle_cast(callback: CallbackQuery) -> None:
    user = callback.from_user
    player = await db.get_or_create_player(user.id, user.username)
    lang = _language(player)
    if player["cast_ready_at"] is not None:
        await callback.answer(i18n.t("already_casting", lang), show_alert=True)
        return
    location = LOCATIONS.get(callback.data.split(":", 1)[1])
    if location is None:
        await callback.answer()
        return
    ready_at = datetime.now(timezone.utc).timestamp() + location.timer_seconds
    await db.start_cast(user.id, location.key, ready_at)
    await callback.message.edit_text(
        i18n.t("line_cast", lang).format(minutes=location.timer_seconds // 60),
        reply_markup=waiting_keyboard(lang),
    )
    await callback.answer()


async def _resolve_pull(
    user_id: int, username: str | None
) -> tuple[str, InlineKeyboardMarkup]:
    player = await db.get_or_create_player(user_id, username)
    lang = _language(player)
    if player["cast_ready_at"] is None:
        return i18n.t("nothing_cast", lang), main_menu_keyboard(lang)
    now = datetime.now(timezone.utc).timestamp()
    if now < player["cast_ready_at"]:
        remaining = int(player["cast_ready_at"] - now)
        text = i18n.t("still_waiting", lang).format(seconds=remaining)
        return text, waiting_keyboard(lang)
    location = LOCATIONS.get(player["cast_location"])
    if location is None:
        await db.clear_cast(user_id)
        return i18n.t("nothing_cast", lang), main_menu_keyboard(lang)
    catch = loot.roll_catch(location)
    caught_at = datetime.now(timezone.utc).isoformat()
    await db.record_catch(user_id, catch, location.key, caught_at)
    await db.clear_cast(user_id)
    text = i18n.t("caught", lang).format(
        species=i18n.t(f"species_{catch.species}", lang),
        rarity=i18n.t(f"rarity_{catch.rarity}", lang),
        weight=catch.weight,
    )
    return text, main_menu_keyboard(lang)


@router.callback_query(F.data == "pull")
async def handle_pull(callback: CallbackQuery) -> None:
    text, keyboard = await _resolve_pull(
        callback.from_user.id, callback.from_user.username
    )
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()


@router.message(Command("check"))
async def handle_check(message: Message) -> None:
    text, keyboard = await _resolve_pull(
        message.from_user.id, message.from_user.username
    )
    await message.answer(text, reply_markup=keyboard)
