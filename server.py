from quart import Quart, websocket
import asyncio


app = Quart(__name__)


@app.route("/")
async def index():
    return "Hello, world!"


@app.websocket("/ws")
async def ws():
    while True:
        await websocket.send("Hello, client!")
        await asyncio.sleep(1)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


    
