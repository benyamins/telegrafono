import os
from pathlib import Path
from dataclasses import dataclass
import logging
import tomlkit

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)


@dataclass
class Config:
    token: str


def load_config() -> Config:
    logger = get_logger(__name__)
    config_path = None
    if os.name == "nt":  # Windows
        config_path = (
            Path("~/AppData").expanduser() / "Local" / "telegrafono" / "config.toml"
        )
    else:  # Linux and other OS
        config_path = Path.home() / ".config" / "telegrafono" / "config.toml"

    try:
        with open(config_path, "r") as f:
            config_data = tomlkit.parse(f.read())
            token = config_data.get("token")
            if not token:
                raise ValueError("Token not found in config file")
            return Config(token=token)
    except FileNotFoundError:
        logger.error(
            "No config file found. Add it in .config or APPDATA/telegrafono/config.toml"
        )
        raise
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        raise
