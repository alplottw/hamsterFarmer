from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    MIN_CLICK: int
    MAX_CLICK: int

    MIN_DELAY: int
    MAX_DELAY: int

    BOOST_ID: str = "BoostFullAvailableTaps"


config = Config()
