from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    MIN_CLICK: int
    MAX_CLICK: int

    MIN_DELAY: int
    MAX_DELAY: int

    BOOST_ID: str = "BoostFullAvailableTaps"
    DAILY_REWARD_ID: str = "streak_days"

    DAILY_CARD_COMBO: list
    DAILY_CARD_COMBO_MAX_PRICE: int

    DAILY_CIPHER: str
    DAILY_CIPHER_TAPS: list

    COLLECT_DAILY: bool
    COLLECT_CIPHER: bool
    COLLECT_COMBO: bool

    COLLECT_CLICKS: bool
    COLLECT_UPGRADES: bool


config = Config()
