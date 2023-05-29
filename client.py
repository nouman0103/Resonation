from fastapi import FastAPI
import datetime
import time
import asyncio, aiohttp
import requests, threading
# import file upload
from fastapi import FastAPI, File, UploadFile, Form
import socket, vlc
import timeit
import ntplib


# create a socket object
app = FastAPI()

class Communicator:
    def __init__(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.connect(('8.8.8.8', 1))
        self.this_ip = sock.getsockname()[0]
        sock.close()
        self.clients = [self.this_ip]
        self.__number_of_sends = 0
        
    
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

    def __unthreaded_File_Upload(self, file, client):
        # send requests.post to audiofile, formdata, file = file
        try:
            r = requests.post(f"http://{client}:8000/audiofile/", files={"file": file})
            print(r.status_code)
            print(r.text)
        except:
            # remove client from list
            self.clients.remove(client)
            print("Client", client, " not reachable")
        
        self.__number_of_sends += 1
    
    def __scanAndSchedule(self):
        while True:
            if self.__number_of_sends == len(self.clients):
                break
            time.sleep(1)
        print("All clients received the file")
        # send timestamp to all clients
        future_time = time.time() + 20
        for client in self.clients:
            try:
                r = requests.get(f"http://{client}:8000/timestamp?timestamp="+str(future_time), timeout=0.5)
            except:
                # remove client from list
                self.clients.remove(client)
                print("Client", client, " not reachable")

        print("Timestamp sent to all clients. Now time:", time.time(), "Future time:", future_time)


    def uploadFile(self, file):
        self.__number_of_sends = 0
        # loop through all client
        for client in self.clients:
            # send file to client
            th = threading.Thread(target=communicator.__unthreaded_File_Upload, args=(file, client))
            th.start()
        
        th = threading.Thread(target=communicator.__scanAndSchedule)
        th.start()
        

def waitAndPlayMusic(timestamp):
    print(timestamp, type(timestamp))
    musicObject = vlc.MediaPlayer("./__audio.mp3")
    c = ntplib.NTPClient()
    response = c.request('pool.ntp.org', version=3)
    time_offset = response.offset
    print("Time offset:", time_offset)
    musicObject.play()
    musicObject.pause()
    musicObject.set_time(0)
    # wait until timestamp
    while True:
        if time.time() >= (timestamp - time_offset):
            break

    print(time.time() + time_offset)
    # play music
    musicObject.play()
    #Timeit the time take to play the music
    #print(timeit.timeit(musicObject.play()))




    #print("Music Started playing")
    # wait until music is finished
    while True:
        # verify the time
        #musicObject.set_time(int((time.time() - timestamp) * 1000))
        time.sleep(1)
    print("Music Finished playing")
    musicObject.stop()
    musicObject.release()
    

communicator = Communicator()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.put("/client")
async def create_client(client: str):
    communicator.addClient(client)
    return {"success": True}


@app.get("/timestamp")
async def timestamp(timestamp: float):
    print("Playing at", datetime.datetime.now() + datetime.timedelta(seconds=time.time() - timestamp))
    th = threading.Thread(target=waitAndPlayMusic, args=(timestamp,))
    th.start()
    return {"success": True}



@app.put("/push_audiofile")
async def push_audiofile(file:UploadFile = File(...)):
    # open file and read it

    file_Data = file.file.read()
    file.file.close()
    # loop through all client
    communicator.uploadFile(file_Data)
    
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
# uvicorn client:app --reload --host 192.168.100.32 --port 8000
