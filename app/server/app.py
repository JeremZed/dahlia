from fastapi import FastAPI, WebSocketDisconnect, WebSocket
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import asyncio
import os
import json

class App():
    def __init__(self, host="127.0.0.1", port=8000, p2p_network=None, ssl_keyfile=None, ssl_certfile=None):
        self.app = FastAPI()

        # Ajouter CORS si nécessaire
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],  # Remplace "*" par tes domaines autorisés en prod
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        self.host = host
        self.port = int(port)
        self.server_thread = None
        self.p2p_network = p2p_network
        self.ssl_keyfile = ssl_keyfile
        self.ssl_certfile = ssl_certfile

        self.ws_clients = set()
        self.static_dir = os.path.join(os.path.dirname(__file__), "../front/dist")

        # Les routes accessibles

        @self.app.get("/")
        async def root():
            return FileResponse(os.path.join(self.static_dir, f"index.html"))

        @self.app.websocket("/ws")
        async def websocket_endpoint(websocket:WebSocket):

            await websocket.accept()
            self.ws_clients.add(websocket)
            try:
                while True:
                    data = await websocket.receive_text()
                    message = json.loads(data)
                    print("[WS] Message reçu:", message)
                    # On propage la mise à jour vers les autres clients WebSocket
                    await self.broadcast_to_websockets(message)
                    # On propage également vers le réseau P2P
                    await self.p2p_network.broadcast(message)

            except WebSocketDisconnect:
                self.ws_clients.remove(websocket)
                print("[WS] Client déconnecté.")

        # Dossier où se trouve l'application js une fois buildé
        self.static_dir = os.path.join(os.path.dirname(__file__), "../front/dist")
        self.app.mount("/", StaticFiles(directory=self.static_dir, html=True), name="static")

    async def broadcast_to_websockets(self, message: dict):
        message_text = json.dumps(message)
        disconnects = set()
        for ws in self.ws_clients:
            try:
                await ws.send_text(message_text)
            except Exception as e:
                print("[WS] Erreur d'envoi à un client:", e)
                disconnects.add(ws)
        for ws in disconnects:
            self.ws_clients.discard(ws)

    async def start_server(self):
        """
            Démarrage du serveur web sous FastApi
        """

        if self.ssl_keyfile is not None:
            if os.path.exists(self.ssl_keyfile) == False:
                raise Exception(f"Fichier {self.ssl_keyfile} n'existe pas.")

        if self.ssl_certfile is not None:
            if os.path.exists(self.ssl_certfile) == False:
                raise Exception(f"Fichier {self.ssl_certfile} n'existe pas.")

        # Démarre la partie P2P en tâche de fond
        if self.p2p_network :
            asyncio.create_task(self.p2p_network.run())

        config = uvicorn.Config(self.app,
                                host=self.host,
                                port=self.port,
                                log_level="info",
                                ssl_keyfile=self.ssl_keyfile,
                                ssl_certfile=self.ssl_certfile
                                )

        server = uvicorn.Server(config)
        await server.serve()

    async def run(self):
        """
            Permet de lancer le serveur web dans un thread
        """
        await self.start_server()
