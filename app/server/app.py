from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
import threading
import os
import time

class App():
    def __init__(self, host="127.0.0.1", port=8000):
        self.app = FastAPI()
        self.host = host
        self.port = int(port)
        self.server_thread = None

        # Dossier où se trouve l'application js une fois buildé
        self.static_dir = os.path.join(os.path.dirname(__file__), "../front/dist")        
        self.app.mount("/", StaticFiles(directory=self.static_dir, html=True), name="static")

        # Les routes accessibles

        @self.app.get("/")
        async def root():
            return FileResponse(os.path.join(self.static_dir, f"index.html"))
        
    def start_server(self):
        """
            Démarrage du serveur web sous FastApi
        """
        
        config = uvicorn.Config(self.app, host=self.host, port=self.port, log_level="info")
        server = uvicorn.Server(config)
        server.run()

    def run(self):
        """
            Permet de lancer le serveur web dans un thread
        """
        self.server_thread = threading.Thread(target=self.start_server, daemon=True)
        self.server_thread.start()
