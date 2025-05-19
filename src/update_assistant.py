"""
This script is used to update the assistant in vapi.
We define the API key, assistant ID in the .env file.
And hit the vapi api endpoint to update the assistant.

only define the changes you want to update using the payload.

Required Environment Variables:
    VAPI_TOKEN: str
    VAPI_ASSISTANT_ID: str

args:
    None

returns:
    True if the assistant is updated successfully, False otherwise.

"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VAPI_TOKEN")
ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")

def update_assistant():
    if not ASSISTANT_ID:
        print("No assistant ID found in .env file. Please create an assistant first.")
        return None
        
    url = f"https://api.vapi.ai/assistant/{ASSISTANT_ID}"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Only include the fields you want to update
    update_payload = {
        "firstMessage": "Hey I am Shizuka from dataverze I just wanted to have a quick confirmation, are you currently available to talk.",
        "voice": {
            "provider": "vapi",
            "voiceId": "Kylie",  # Update to match the new voice
            "chunkPlan": {
                "enabled": True,
                "minCharacters": 30
            }
        }
    }
    
    try:
        response = requests.patch(url, headers=headers, json=update_payload)
        response.raise_for_status()
        print(f"Assistant {ASSISTANT_ID} updated successfully!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error updating assistant: {e}")
        return False

if __name__ == "__main__":
    update_assistant()