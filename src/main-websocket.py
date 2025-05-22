from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import JSONResponse
from collections import defaultdict
import datetime
import csv
import os
import uvicorn

app = FastAPI()

# Store chat logs in memory
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

@app.websocket("/vapi")
async def vapi_websocket(websocket: WebSocket):
    await websocket.accept()
    
    try:
        while True:
            # Receive Vapi event
            data = await websocket.receive_json()
            message = data.get("message", {})
            event_type = message.get("type")

            if event_type == "end-of-call-report":
                # Process end-of-call-report
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

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.close()

@app.get("/health")
async def health_check():
    return JSONResponse(content={"status": "ok"})

if __name__ == "__main__":
    # Run FastAPI server locally on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)