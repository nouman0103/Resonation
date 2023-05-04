from fastapi import FastAPI
import datetime
import time
import asyncio, aiohttp
import requests, threading
# import file upload
from fastapi import FastAPI, File, UploadFile, Form
import socket

# create a socket object
app = FastAPI()

class Communicator:
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 1))
        self.this_ip = sock.getsockname()[0]
        sock.close()
        self.clients = [self.this_ip]
    
    def addClient(self, client):
        # check if client is already in the list
        if client not in self.clients:
            self.clients.append(client)


    def connectToClient(self, host):
        try:
            # send put request to client
            r = requests.put(f"http://{host}:8000/client?client="+communicator.this_ip, timeout=1)
            self.addClient(host)
        except Exception as e:
            pass

    def shine(self):
        for i in range(255):
            # create a client
            host = communicator.this_ip.rsplit(".", 1)[0] + "." + str(i)
            # send a request to the client
            th = threading.Thread(target=communicator.connectToClient, args=(host,))
            th.start()
            
    async def broadcast(self):
        ...
    


communicator = Communicator()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.put("/client")
async def create_client(client: str):
    communicator.addClient(client)
    return {"success": True}


@app.get("/timestamp")
async def timestamp():
    # return 3 sec later
    return {"timestamp": time.time() + 3}

@app.put("/push_audiofile")
async def push_audiofile(file:UploadFile = File(...)):
    # open file and read it
    

    # loop through all client
    for client in communicator.clients:
        # send file to client
        try:
            print("Trying to send file to client: ", client)
            # upload using aiohttp
            async with aiohttp.ClientSession() as session:
                # upload file as form data
                async with session.post(f"http://{client}:8000/audiofile/", data={"file": file.file}) as resp:
                    print(resp.status)
                    print(await resp.text())
                    
        except Exception as e:
            print(e)
            # remove client from list
            communicator.clients.remove(client)
        
        

    return {"success": True}


@app.post("/audiofile/")
async def create_upload_file(file: UploadFile = File(...)):
    # save file
    with open("./__audio.mp3", "wb") as f:
        f.write(file.file.read())

    return {"filename": file.filename}


@app.get("/runclient")
async def runclient():
    pass

"""

"""

# on server start



@app.on_event("startup")
async def startup_event():
    print("Server is starting up...")
    th = threading.Thread(target=communicator.shine)
    th.start()
    
@app.get("/clients")
async def clients():
    return {"clients": communicator.clients}

# Run the server

# uvicorn client:app --reload --host 0.0.0.0 --port 8000
