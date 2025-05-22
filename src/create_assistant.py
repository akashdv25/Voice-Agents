"""

This is the code to create a new assistant in vapi.
More details can also  be configured.

Required Environment Variables:
    VAPI_TOKEN: str

Args:
    None

Returns:
    assistant_id: str

"""

import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("VAPI_TOKEN")

def create_assistant():
    url = "https://api.vapi.ai/assistant"
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Define the system prompt
    system_prompt = """
    [Identity]  
    You are a strict and professional voice assistant focused on confirming the user's identity details.

    [Style]  
    - Maintain a formal and efficient tone.  
    - Use concise and direct language.  
    - Be polite yet firm in guiding the conversation.

    [Response Guidelines]  
    - Avoid engaging in casual chat; reiterate the verification purpose.

    [Task & Goals]  
    1. Greet the user and ask, "Are you {{ name }}?" <wait for the response>  
    2. If the user indicates they are busy, respond with, "Thanks, will call you later," and silently end the call.  
    3. If the conversation proceeds, ask, "Is your place of stay {{ place }}?"  
    4. After confirming end the call with end_call tool

    [Error Handling / Fallback]  
    - If the user says "I can't talk right now," respond with, "Thanks, will call you later," and silently end the call.  
    - If no response is detected for 5 seconds, say "No response detected," and silently end the call.  
    - If the user says "bye," silently end the call.  
    - If unable to confirm the details after three attempts, say, "We couldn't complete the verification. Please try again later. Goodbye," and silently end the call.

"""
    
    payload = {
        "name": "Sasha",
        "transcriber": {
            "provider": "deepgram",
            "model": "nova-3",
            "language": "en",
            "confidenceThreshold": 0.4,
        },
        "model": {
            "provider": "openai",  
            "model": "gpt-4o-mini", 
            "fallbackModels":["gpt-4.1","gpt-4.1-nano"],
            "messages": [
                {
                    "role": "system",
                    "content": system_prompt
                }
            ],
            "temperature": 0.2,
            "maxTokens": 250,
            "tools": [
        {
            "type": "endCall",
            "function": {
                "name": "end_call",
                "description": "End the current call",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "message": {
                            "type": "string",
                            "description": "ummm...Thanks ...Have a Great Day"
                        }
                    }
                }
            }
        }
    ]
        },
        "voice": {
            "provider": "vapi",  
            "voiceId": "Neha",  
            "cachingEnabled": True,

        },
        "firstMessage": "Hey I am Sasha from dataverze I just wanted to have a quick confirmation, are you currently available to talk.",
        "firstMessageMode": "assistant-speaks-first",
        "silenceTimeoutSeconds": 10,
        "maxDurationSeconds": 30,  
        "endCallMessage": "um..thanks for your time , have a great day",
        "endCallPhrases": [
            "bye", 
            "goodbye",
            "see you later",
            "Have a great day"
        ],
        
        "monitorPlan": {
            "listenEnabled": True,
            "controlEnabled": True
        },
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        response_data = response.json()
        
        # Extract the assistant ID from the response
        assistant_id = response_data.get('id')
        
        if assistant_id:
            print(f"Assistant created successfully!")
            print(f"Assistant ID: {assistant_id}")
            
            # Save the assistant ID to .env file
            with open('.env', 'a') as env_file:
                env_file.write(f"\nVAPI_ASSISTANT_ID='{assistant_id}'")
            
            return assistant_id
        else:
            print("Error: No assistant ID in response")
            print("Full response:", response_data)
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Error creating assistant: {e}")
        return None

if __name__ == "__main__":
    create_assistant()
