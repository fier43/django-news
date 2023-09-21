import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=Path(".env"))  # Переменные (пароли, ИД) из файла .env


PASSWORD_DB = os.environ.get("PASSWORD_DB")


# При указании * чтобы передавались только эти переменные
__all__ = "PASSWORD_DB"
