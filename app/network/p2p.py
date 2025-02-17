import asyncio
import json
import socket

class P2PNetwork():

    def __init__(self, port, discovery_port, discovery_interval):

        # Configuration du réseau
        self.port = int(port)
        self.discovery_port = int(discovery_port)
        self.discovery_interval = int(discovery_interval)

        # List des paires du réseau
        self.know_peers = set()

        # Fonction callback sur l'event message
        self.on_message = None

    async def handle_connection(self, reader, writer):
        try:
            data = await reader.read(1024)
            if data:
                message = json.loads(data.decode())
                peer_ip = writer.get_extra_info('peername')[0]

                print(f"[P2P] Message reçu de {peer_ip}: {message}")

                local_ip = self.get_local_ip()
                if peer_ip != local_ip:
                    self.know_peers.add(peer_ip)

                # On exécute la fonction callback
                if self.on_message:
                    await self.on_message(message)

        except Exception as e:
            print("[P2P] Erreur de connexion:", e)
        finally:
            writer.close()
            await writer.wait_closed()

    async def start_server(self):
        server = await asyncio.start_server(self.handle_connection, "0.0.0.0", self.port)
        address = ", ".join( str(sock.getsockname()) for sock in server.sockets)

        print(f"[P2P] Serveur démarré sur: {address}")
        async with server:
            await server.serve_forever()

    async def broadcast(self, message: dict):
        """

            Permet d'envoyer un message à tous les pairs connus

        """
        message_text = json.dumps(message)
        for peer in list(self.know_peers):
            try:
                reader, writer = await asyncio.open_connection(peer, self.port)
                writer.write(message_text.encode())
                await writer.drain()
                writer.close()
                await writer.wait_closed()
            except Exception as e:
                print(f"[P2P] Erreur de l'envoi à {peer}: {e}")
                self.know_peers.discard(peer)

    async def network_discovery(self):
        """
            Permet de diffuser régulièrement son adresse et écoute les diffusions
            des pairs afin de découvrir automatiquement les autres clients sur le réseau.
        """
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.bind(("", self.discovery_port))
        sock.setblocking(False)

        local_ip = self.get_local_ip()
        while True:
            discovery_message = json.dumps({"peer": local_ip})
            try:
                sock.sendto(discovery_message.encode(), ('<broadcast>', self.discovery_port))
            except Exception as e:
                print("[P2P] Erreur du broadcast:", e)
            try:
                # Tenter de recevoir les diffusions sans bloquer
                while True:
                    data, addr = sock.recvfrom(1024)
                    message = json.loads(data.decode())
                    peer_ip = message.get("peer")
                    if peer_ip and peer_ip != local_ip and peer_ip not in self.know_peers:
                        self.know_peers.add(peer_ip)
                        print(f"[P2P] Nouveau pair découvert: {peer_ip}")
            except BlockingIOError:
                # Pas de données disponibles pour le moment
                pass
            await asyncio.sleep(self.discovery_interval)


    def get_local_ip(self) -> str:
        """
            Permet de récupèrer l'adresse IP de la machine.
        """
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
        except Exception:
            local_ip = "127.0.0.1"
        finally:
            s.close()
        return local_ip

    async def run(self):

        server = asyncio.create_task(self.start_server())
        discovery = asyncio.create_task(self.network_discovery())

        await asyncio.gather(server, discovery)