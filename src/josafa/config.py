from os import getenv

class Config:
    # Bot
    BOT_DEFAULT_PREFIX: str = getenv("BOT_DEFAULT_PREFIX")
    BOT_DISCORD_TOKEN: str = getenv("BOT_DISCORD_TOKEN")

    # MongoDB
    MONGODB_DATABASE: str = getenv("MONGODB_DATABASE")
    MONGODB_HOST: str = getenv("MONGODB_HOST")
    MONGODB_USERNAME: str = getenv("MONGODB_USERNAME")
    MONGODB_PASSWORD: str = getenv("MONGODB_PASSWORD")
