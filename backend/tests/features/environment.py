import logging
import os
from dotenv import load_dotenv


def before_all(context):
    env_path = os.path.join(os.path.dirname(__file__), "../../.env")
    if os.path.exists(env_path):
        load_dotenv(env_path)
        logging.info("Loaded environment variables from .env")
    else:
        logging.info(f"No .env file found at {env_path}")
