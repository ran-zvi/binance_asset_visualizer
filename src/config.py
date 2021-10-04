from dataclasses import dataclass

import os

BINANCE_API_KEY = "BINANCE_API_KEY"
BINANCE_SECRET_KEY = "BINANCE_SECRET_KEY"


@dataclass
class Config:
    binance_api_key: str
    binance_secret_key: str

    @classmethod
    def create_from_env_vars(cls) -> "Config":
        api_key = os.environ[BINANCE_API_KEY]
        secret_key = os.environ[BINANCE_SECRET_KEY]

        return Config(api_key, secret_key)

config = Config.create_from_env_vars()