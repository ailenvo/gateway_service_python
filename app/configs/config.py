import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", default="DEV")
PORT = int(os.getenv("PORT", default="8000"))
