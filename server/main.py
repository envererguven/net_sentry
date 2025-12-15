from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    return """
    <html>
        <head>
            <title>Target Acquired</title>
            <style>
                body { background-color: #0f0f0f; color: #00ff00; font-family: 'Courier New', monospace; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }
                .container { text-align: center; border: 2px solid #00ff00; padding: 20px; box-shadow: 0 0 10px #00ff00; }
                h1 { text-transform: uppercase; letter-spacing: 5px; animation: blink 1s infinite; }
                @keyframes blink { 50% { opacity: 0; } }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Target Online</h1>
                <p>System operational. Waiting for incoming transmission...</p>
            </div>
        </body>
    </html>
    """

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
