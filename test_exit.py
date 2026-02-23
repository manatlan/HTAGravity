import asyncio
import httpx
from htag.server import WebServer
from htag.core import Tag
import threading
import uvicorn
import time

class DummyApp(Tag.App):
    pass

async def test():
    app = WebServer(DummyApp)
    
    def run_server():
        uvicorn.run(app.app, host="127.0.0.1", port=8123, log_level="warning")
        
    t = threading.Thread(target=run_server, daemon=True)
    t.start()
    await asyncio.sleep(1) # wait for server
    
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8123") as client:
        # Get cookie
        r = await client.get("/")
        print("Connected:", r.status_code)
        
        # Connect SSE
        async with client.stream("GET", "/stream") as response:
            print("SSE Connected")
            # Exiting context immediately triggers disconnect
            
    print("Client disconnected, waiting for server to auto-exit...")
    # The server has a 0.5s delay before os._exit(0)
    await asyncio.sleep(2)
    print("FAILED: Server is still alive")

if __name__ == "__main__":
    asyncio.run(test())
