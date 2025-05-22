from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from collections import defaultdict
import datetime
import csv
import os

'''
This is the main file that will be used to handle the webhook from vapi.
It will save the call logs to a csv file.

I created a fastapi app and used the post method to handle the webhook , 
to send data from vapi server we need ngrok to expose the local server to the internet, 
to recieve responses , web hook url is used.

after the call is ended , the server events responses from vapi are saved to a csv file locally

'''


app = FastAPI()

chat_logs = defaultdict(list)

# Define the CSV file name
CSV_FILE = "calls.csv"

# Initialize the CSV file with headers if it doesn't exist
if not os.path.exists(CSV_FILE):
    with open(CSV_FILE, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=[
            "call_id", "timestamp", "summary", "transcript", "recording_url", "chat_log"
        ])
        writer.writeheader()

@app.post("/webhook")
async def vapi_webhook(request: Request):
    data = await request.json()
    message = data.get("message", {})
    event_type = message.get("type")

    if event_type == "end-of-call-report":
        call = message.get("call", {})
        call_id = call.get("id", "unknown")
        summary = message.get("summary", "")
        transcript = message.get("transcript", "")
        recording_url = message.get("recordingUrl", "")
        messages = message.get("messages", [])

        # Save messages to chat_logs
        for msg in messages:
            chat_logs[call_id].append({
                "role": msg.get("role", "unknown"),
                "message": msg.get("message", ""),
                "timestamp": datetime.datetime.now().isoformat()
            })

        # Combine messages into a single chat log string
        chat_str = "\n".join([
            f"[{m['role'].capitalize()}]: {m['message']}"
            for m in chat_logs[call_id]
        ])

        # Save to CSV
        with open(CSV_FILE, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=[
                "call_id", "timestamp", "summary", "transcript", "recording_url", "chat_log"
            ])
            writer.writerow({
                "call_id": call_id,
                "timestamp": datetime.datetime.now().isoformat(),
                "summary": summary,
                "transcript": transcript,
                "recording_url": recording_url,
                "chat_log": chat_str
            })

        # Print output
        print(f"\n📞 Call Ended! ID: {call_id}")
        print(f"Saved to CSV ✅")
        print(f"Recording: {recording_url}")
        print(f"Summary: {summary}")
        print(f"Transcript: {transcript}")
        print("Chat log:")
        print(chat_str)
        print("-" * 60)

    return JSONResponse(content={"status": "ok"})
