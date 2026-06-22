DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ("ru", "en")

TEXTS = {
    "welcome": {
        "ru": "Добро пожаловать на рыбалку! Закидывай удочку и смотри, что клюнет.",
        "en": "Welcome to the fishing game! Cast your line and see what bites.",
    },
    "cast_pond_button": {
        "ru": "🎣 Закинуть в пруд",
        "en": "🎣 Cast at the pond",
    },
    "pull_button": {
        "ru": "🎣 Тащить!",
        "en": "🎣 Pull!",
    },
    "line_cast": {
        "ru": "Удочка заброшена ({location}). Возвращайся через {minutes} мин.",
        "en": "Line cast ({location}). Come back in {minutes} min.",
    },
    "location_pond": {"ru": "пруд", "en": "pond"},
    "bite": {
        "ru": "🐟 Клёв! Пора тащить!",
        "en": "🐟 Bite! Time to pull!",
    },
    "still_waiting": {
        "ru": "Пока не клюёт... осталось ~{seconds} с.",
        "en": "Not biting yet... ~{seconds}s left.",
    },
    "nothing_cast": {
        "ru": "У тебя нет заброшенной удочки. Сначала закинь.",
        "en": "You have no line in the water. Cast first.",
    },
    "already_casting": {
        "ru": "Удочка уже заброшена.",
        "en": "Your line is already in the water.",
    },
    "caught": {
        "ru": "Поймал: {species} ({rarity}), {weight} кг!",
        "en": "You caught: {species} ({rarity}), {weight} kg!",
    },
    "rarity_common": {"ru": "обычная", "en": "common"},
    "rarity_uncommon": {"ru": "необычная", "en": "uncommon"},
    "rarity_rare": {"ru": "редкая", "en": "rare"},
    "rarity_legendary": {"ru": "легендарная", "en": "legendary"},
    "species_crucian": {"ru": "карась", "en": "crucian carp"},
    "species_perch": {"ru": "окунь", "en": "perch"},
}


def t(key: str, lang: str) -> str:
    translations = TEXTS.get(key)
    if translations is None:
        return key
    return translations.get(lang, translations.get(DEFAULT_LANGUAGE, key))
