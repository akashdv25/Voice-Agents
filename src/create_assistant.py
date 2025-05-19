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
    1. Greet the user and ask, "Are you Anant Chaudhary?" <wait for the response>  
    2. If the user indicates they are busy, respond with, "Thanks, will call you later," and silently end the call.  
    3. If the conversation proceeds, ask, "Is your place of stay Pune?"  
    4. Regardless of the response, say, "Thanks for the confirmation," and then silently end the call.  
    5. Always end the call silently after confirming the details or handling the user's availability.

    [Error Handling / Fallback]  
    - If the user says "I can't talk right now," respond with, "Thanks, will call you later," and silently end the call.  
    - If no response is detected for 5 seconds, say "No response detected," and silently end the call.  
    - If the user says "bye," silently end the call.  
    - If unable to confirm the details after three attempts, say, "We couldn’t complete the verification. Please try again later. Goodbye," and silently end the call.

"""
    
    payload = {
    "name": "Dataverze Customer Support Assistant",
    "transcriber": {
        "provider": "deepgram",
        "language": "en",
        "model": "nova-3"
       
    },
    "model": {
        "provider": "openai",
        "model": "gpt-4",  # Make sure to use a valid model name
        "emotionRecognitionEnabled": True,
        "messages": [
        {
            "role": "system",
            "content": system_prompt
        }
    ],
        "temperature": 0.7,
        "maxTokens": 150
    },
    "voice": {
        "provider": "vapi",
        "voiceId": "Kylie",  
        "chunkPlan": {
            "enabled": True,
            "minCharacters": 30
        }
    },
    "firstMessage": "Hey I am Shizuka from dataverze I just wanted to have a quick confirmation, are you currently available to talk.",
    "firstMessageMode": "assistant-speaks-first",
    "monitorPlan": {
        "listenEnabled": True,
        "controlEnabled": True
    },
    "silenceTimeoutSeconds": 10,
    "endCallMessage": "Thanks for the confirmation , Have a great day",
    "endCallPhrases": [
        "bye", 
        "goodbye",
        "see you later",
        "Have a great day"
        ],
    "artifactPlan": {
        "recordingEnabled": True,
        "transcriptPlan": {
            "enabled": True,
            "assistantName": "AI Assistant",
            "userName": "Customer"
        }
    }
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
