from dotenv import load_dotenv
import os

# Load environment variables from the .env file
load_dotenv()

class Config:
    PORT_SERVER = int(os.getenv("PORT_SERVER", 8000))  # Default to 8000 if not set
    AGENT_HOST_NAME = os.getenv("AGENT_HOST_NAME", "localhost")
    SERVICE_NAME = os.getenv("SERVICE_NAME", "default-service")
    VERSION_API = os.getenv("VERSION", "v1")
    PROMETHUES_PORT = int(os.getenv("PROMETHUES_PORT", 9090))  # Default to 9090 if not set
