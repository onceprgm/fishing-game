import random
from dataclasses import dataclass

from bot.game.locations import Location

RARITY_WEIGHTS = {
    "common": 60,
    "uncommon": 25,
    "rare": 12,
    "legendary": 3,
}

RARITY_COIN_MULTIPLIER = {
    "common": 1.0,
    "uncommon": 2.0,
    "rare": 5.0,
    "legendary": 15.0,
}

COINS_PER_KG = 50


@dataclass(frozen=True)
class Catch:
    species: str
    rarity: str
    weight: float
    coins: int


def roll_catch(location: Location) -> Catch:
    species = random.choice(location.species)
    rarity = random.choices(
        list(RARITY_WEIGHTS), weights=list(RARITY_WEIGHTS.values())
    )[0]
    weight = round(random.uniform(species.min_weight, species.max_weight), 2)
    coins = round(weight * COINS_PER_KG * RARITY_COIN_MULTIPLIER[rarity])
    return Catch(species=species.key, rarity=rarity, weight=weight, coins=coins)
