import os
from typing import Dict, Optional

from dotenv import dotenv_values


class EnvLoader:
    """
    A class for loading environment variables from a .env file that start with a specified prefix.

    Args:
        filename (str, optional): The path to the .env file. Defaults to ".env".
        prefix (str, optional): The prefix for environment variables to load. Defaults to "".
    """

    def __init__(
        self, filename: Optional[str] = ".env", prefix: Optional[str] = ""
    ) -> None:
        self.filename = filename
        self.prefix = prefix

    def load(self) -> None:
        """Load environment variables from the .env file that start with the specified prefix."""

        env_vars = dotenv_values(self.filename)
        for key, value in env_vars.items():
            if key.startswith(self.prefix):
                os.environ[key] = value

    def build(self) -> Dict[str, str]:
        """Build a dictionary with the environment variables that start with the specified prefix."""

        self.load()

        env_vars = dotenv_values(self.filename)
        prefix_len = len(self.prefix)
        filtered_vars = {
            key[prefix_len:].lower(): value
            for key, value in env_vars.items()
            if key.startswith(self.prefix)
        }

        return filtered_vars
