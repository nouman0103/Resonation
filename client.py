import websockets
import asyncio
import socket

async def hello():
    host = socket.gethostname()
    print(host)
    ip = socket.gethostbyname(host)
    print(ip)

    uri = "ws://"+ip+":5000/ws"
    async with websockets.connect(uri) as websocket:
        while True:
            greeting = await websocket.recv()
            print(f"< {greeting}")

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.create_task(hello())
loop.run_forever()