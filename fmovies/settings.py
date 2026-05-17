import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

FM_URL = os.getenv("FM_URL", "https://fmoviess.org")
