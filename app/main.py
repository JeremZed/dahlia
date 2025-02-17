from server.app import App
from client.main import client_start
import os
from dotenv import load_dotenv

from network.p2p import P2PNetwork
import asyncio
import threading

async def run_server():
    try:

        load_dotenv()

        p2p_network = P2PNetwork(
            port=os.getenv('NETWORK_P2P_PORT'),
            discovery_port=os.getenv('NETWORK_UDP_DISCOVERY_PORT'),
            discovery_interval=os.getenv('NETWORK_DISCOVERY_INTERVAL')
        )

        # Gestion du SSL
        if os.getenv('FASTAPI_SSL_ENABLED') == 'true':
            ssl_keyfile = os.getenv('FASTAPI_SSL_KEYFILE')
            ssl_certfile = os.getenv('FASTAPI_SSL_CERTFILE')
        else:
            ssl_keyfile = None
            ssl_certfile = None

        app_web = App(
            host=os.getenv('FASTAPI_IP'),
            port=os.getenv('FASTAPI_PORT'),
            p2p_network=p2p_network,
            ssl_certfile=ssl_certfile,
            ssl_keyfile=ssl_keyfile
        )

        await app_web.run()

    except KeyboardInterrupt:
        print("Arrêt de l'application")

def start_server():
    asyncio.run(run_server())

if __name__ == "__main__":

    # Lancer le serveur dans un thread séparé
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()

    client_start()