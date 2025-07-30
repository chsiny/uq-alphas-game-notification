import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Ultramsg API Configuration
# Get your credentials from https://ultramsg.com/
# Set these in your .env file or as environment variables

ULTRA_MSG_TOKEN = os.getenv("ULTRA_MSG_TOKEN", "your_token_here")
ULTRA_MSG_INSTANCE_ID = os.getenv("ULTRA_MSG_INSTANCE_ID", "your_instance_id_here")
DEFAULT_PHONE_NUMBER = os.getenv("DEFAULT_PHONE_NUMBER", "+61423339538")
DEFAULT_GROUP_ID = os.getenv("DEFAULT_GROUP_ID", "120363402721471065@g.us") 