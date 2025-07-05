from dataclasses import dataclass
from typing import Dict


@dataclass
class RohlikCredentials:
    """Class containing Rohlik credentials."""

    email: str
    password: str
    name: str = ""

    def __post_init__(self):
        self.password = HiddenString(self.password)

    @classmethod
    def from_environ(cls, *, use_dotenv=False):
        """Create object using credentials from environment variables."""
        import os

        if use_dotenv:
            from dotenv import load_dotenv

            load_dotenv()
        return cls(email=os.environ["ROHLIK_EMAIL"], password=os.environ["ROHLIK_PASSWORD"])

    def to_dict(self) -> Dict[str, str]:
        """Convert data to a dictionary."""
        return {"email": self.email, "password": self.password, "name": self.name}


class HiddenString(str):
    """Class for hiding values in __repr__ method."""

    def __repr__(self):
        return "********".__repr__()
