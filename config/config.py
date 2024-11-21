# config.py
from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

class Config:
    PORT_SERVER = int(os.getenv("PORT_SERVER"))
    AGENT_HOST_NAME = os.getenv("AGENT_HOST_NAME", "localhost")
    SERVICE_NAME = os.getenv("SERVICE_NAME")
    VERSION_API = os.getenv("VERSION")
