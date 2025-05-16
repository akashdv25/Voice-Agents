import requests
import os
from dotenv import load_dotenv

load_dotenv()

'''
This script is used to make a call to a customer using the Vapi API.
We define the API key, assistant ID,  and phone number ID in the .env file.
And hit the vapi api endpoint to make the call.

We can use either vapi or twilio to make the call.

'''


API_KEY = os.getenv("VAPI_TOKEN")
ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")
CUSTOMER_NUMBER = "+917000120198"
PHONE_NUMBER_ID=os.getenv("PHONE_NUMBER_ID")



url = "https://api.vapi.ai/call"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

payload = {
    "assistantId": ASSISTANT_ID,
    "phoneNumberId": PHONE_NUMBER_ID,
    "customer": {
        "number": CUSTOMER_NUMBER
    }
}

response = requests.post(url, headers=headers, json=payload)

print(f"Status: {response.status_code}")
print("Response:", response.json())
