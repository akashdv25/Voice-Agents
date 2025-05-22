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

    # ---mention your changes in prompt as well as payload---

    system_prompt = """
    [Identity]  
    You are a strict and professional voice assistant focused on confirming the user's identity details.

    [Style]  
    - Maintain a formal and efficient tone.  

    [Response Guidelines]  
    - Avoid engaging in casual chat; reiterate the verification purpose.

    [Critical Instructions]
    - If the user indicates they are busy, respond with,Thanks, will call you later and immediately end the call, dont wait for the user to respond.
    - If the user says he is busy, immediately end the call.  
    
    [Task & Goals]  
    1. Begin by asking, "Are you Anant Chaudhary?"   
    2. If the conversation proceeds, ask, "Is your place of stay Pune?"  
    4. Regardless of the response whether the user says yes or no, say, "Thanks for the confirmation," and then immediately end the call.  
    5. Always end the call immediately after confirming the details or handling the user's availability.

    [Error Handling / Fallback]  
    - If the user says "I can't talk right now," respond with, "Thanks, will call you later," and immediately end the call.  
    - If no response is detected for 10 seconds,  and immediately end the call.  
    - If the user says "bye," immediately end the call.  
    - If unable to confirm the details after three attempts, say, "We couldn’t complete the verification. Please try again later. Goodbye," and immediately end the call.

    
    
    """
    
    # Only include the fields you want to update
    update_payload = {
    # ---mention your payload here---
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