# Standard Libraries
import os
import logging

# Non-Standard Libraries
from dotenv import load_dotenv

load_dotenv() # Load environment variables from a .env file. This is crucial for keeping sensitive data like API keys out of your main codebase.

logging.basicConfig(level=logging.ERROR) 

MODEL_GEMINI = "gemini-2.0-flash" # Specifies the Google Gemini model to be used by the ADK agent.
APP_NAME_FOR_ADK = "chat_app" # A unique name for your application within ADK, used for session management.
USER_ID = "charlescro" # A default user ID. In a real application, this would be dynamic (e.g., from a login system).

INITIAL_STATE = {}
MESSAGE_HISTORY_KEY = "messages_final_mem_v2" # Key used by Streamlit to store the chat history in its session state.
ADK_SESSION_KEY = "adk_session_id" # Key used by Streamlit to store the unique ADK session ID.

def get_api_key():
    """Retrieves the Google API Key from environment variables."""
    api_key = os.environ.get("GOOGLE_API_KEY")
    # Basic check to ensure the key is present and not the placeholder.
    if not api_key or "YOUR_GOOGLE_API_KEY" in api_key:
        return None
    return api_key