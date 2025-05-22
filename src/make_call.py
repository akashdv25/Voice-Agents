
'''
We can use the vapi python library to make the call as well directly
it abstracts the http calls and provides a more pythonic way to make the call.

Args:
    None

Returns:

    response: dict

Required Environment Variables:
    VAPI_TOKEN: str
    VAPI_ASSISTANT_ID: str
    PHONE_NUMBER_ID: str
    CUSTOMER_NUMBER: str

'''


import os
from vapi import Vapi
from dotenv import load_dotenv

load_dotenv()

def make_call():
    # Get environment variables
    API_KEY = os.getenv("VAPI_TOKEN")
    ASSISTANT_ID = os.getenv("VAPI_ASSISTANT_ID")
    PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
    CUSTOMER_NUMBER = "+917000120198"  

    # Check if required environment variables are present
    if not all([API_KEY, ASSISTANT_ID, PHONE_NUMBER_ID]):
        print("Error: Missing required environment variables")
        print(f"API_KEY: {'Present' if API_KEY else 'Missing'}")
        print(f"ASSISTANT_ID: {'Present' if ASSISTANT_ID else 'Missing'}")
        print(f"PHONE_NUMBER_ID: {'Present' if PHONE_NUMBER_ID else 'Missing'}")
        return None

    try:
        # Initialize VAPI client
        client = Vapi(token=API_KEY)

        # Create call
        call_data = {
            "assistant_id": ASSISTANT_ID,
            "phone_number_id": PHONE_NUMBER_ID,
            "customer": {
                "number": "+917000120198"
            },
    #         "customers": [
    #     {
    #         "number": "+917000120198"
    #     },
    #     {
    #         "number": "+918076120997"
    #     }
    # ],
        }
        
        response = client.calls.create(**call_data)
        
        print("\nCall initiated successfully!")
        print("------------------------")
        print(f"Call ID: {response.id}")
        print(f"Status: {response.status}")
        print(f"Created At: {response.created_at}")
        print(f"Phone Call Provider: {response.phone_call_provider}")
        print(f"Provider Call ID: {response.phone_call_provider_id}")
        if response.monitor:
            print(f"Monitor Listen URL: {response.monitor.listen_url}")
        print("------------------------\n")
        
        return response
        

    except Exception as e:
        print(f"Error making call: {e}")
        return None

if __name__ == "__main__":
    make_call()