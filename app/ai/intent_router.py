import requests
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

CANDIDATE_LABELS = [
    "search_products",
    "place_order",
    "update_profile",
    "get_order_status"
]

def get_headers():
    """Get headers with the HF API token."""
    token = os.getenv("HF_API_TOKEN")
    if not token:
        logger.error("HF_API_TOKEN not found in environment variables")
        raise ValueError("HF_API_TOKEN not found in environment variables")
    return {"Authorization": f"Bearer {token}"}

def detect_intent_with_ai(message: str) -> str:
    try:
        headers = get_headers()
        payload = {
            "inputs": message,
            "parameters": {
                "candidate_labels": CANDIDATE_LABELS
            }
        }

        logger.debug(f"Making request to {API_URL}")
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()

        if "error" in result:
            logger.error(f"Hugging Face API error: {result['error']}")
            return "unknown"

        return result["labels"][0]
    except Exception as e:
        logger.error(f"Error in detect_intent_with_ai: {str(e)}")
        return "unknown"
