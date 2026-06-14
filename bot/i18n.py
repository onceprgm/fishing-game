DEFAULT_LANGUAGE = "en"
SUPPORTED_LANGUAGES = ("ru", "en")

TEXTS = {
    "welcome": {
        "ru": "Добро пожаловать на рыбалку! Закидывай удочку и смотри, что клюнет.",
        "en": "Welcome to the fishing game! Cast your line and see what bites.",
    },
}


def t(key: str, lang: str) -> str:
    translations = TEXTS[key]
    return translations.get(lang, translations[DEFAULT_LANGUAGE])
