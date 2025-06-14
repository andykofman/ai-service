import requests
import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

HF_API_TOKEN = os.getenv("HF_API_TOKEN")  # Store your token in .env or OS env
logger.debug(f"HF_API_TOKEN loaded: {'Yes' if HF_API_TOKEN else 'No'}")

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-mnli"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}"
}

CANDIDATE_LABELS = [
    "search_products",
    "place_order",
    "update_profile",
    "get_order_status"
]

def detect_intent_with_ai(message: str) -> str:
    payload = {
        "inputs": message,
        "parameters": {
            "candidate_labels": CANDIDATE_LABELS
        }
    }

    logger.debug(f"Making request to {API_URL} with headers: {HEADERS}")
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    result = response.json()

    if "error" in result:
        logger.error(f"Hugging Face API error: {result['error']}")
        return "unknown"

    return result["labels"][0]
