from fastapi import FastAPI
import uvicorn
import threading

class App():
    def __init__(self, host="127.0.0.1", port=8000):
        self.app = FastAPI()
        self.host = host
        self.port = int(port)
        self.server_thread = None

        # Les routes accessibles

        @self.app.get("/")
        async def root():
            return {"message": "Hello World"}
        
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
