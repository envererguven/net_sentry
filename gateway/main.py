from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import threading
import asyncio
import json
from database import init_db, get_recent_packets
from sniffer import start_sniffer, packet_queue
import os

app = FastAPI(title="NetSentry Gateway")

# CORS for React Frontend
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="NetSentry Gateway")

# Serve Frontend
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def read_index():
    return FileResponse("frontend/index.html")

# Background Sniffer Thread
def run_sniffer_thread():
    try:
        # Give DB a moment to init if thread starts super fast (redundant with startup event but safe)
        import time
        time.sleep(2)
        start_sniffer(interface="eth0")
    except Exception as e:
        print(f"Sniffer crashed: {e}")

import queue
packet_thread_queue = queue.Queue()

@app.on_event("startup")
async def startup_event():
    # Initialize DB explicitly on startup
    init_db()
    
    # Start the sniffer in a background thread
    t = threading.Thread(target=run_sniffer_thread, daemon=True)
    t.start()
    
    # Start the bridge task to move packets from thread-safe queue to async broadcast
    asyncio.create_task(broadcast_packets())

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                self.disconnect(connection)

manager = ConnectionManager()

async def broadcast_packets():
    while True:
        # Get from asyncio queue (populated by sniffer logic)
        packet = await packet_queue.get()
        await manager.broadcast(json.dumps(packet))

@app.get("/api/history")
async def get_history():
    return get_recent_packets()

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text() # Keep connection open
    except WebSocketDisconnect:
        manager.disconnect(websocket)
