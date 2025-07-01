import os
from dotenv import load_dotenv

load_dotenv()

ENV = os.getenv("ENV", default="DEV")
PORT = os.getenv("PORT", default="8000")
USER_SERVICE = os.getenv("USER_SERVICE")
AUTH_SERVICE = os.getenv("AUTH_SERVICE")
PRODUCT_SERVICE = os.getenv("PRODUCT_SERVICE")
