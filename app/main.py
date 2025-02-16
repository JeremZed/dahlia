from server.app import App
from client.main import client_start
import os
from dotenv import load_dotenv

if __name__ == "__main__":
    try:

        load_dotenv()

        app_web = App(host=os.getenv('FASTAPI_IP'), port=os.getenv('FASTAPI_PORT'))
        app_web.run()  

        client_start()  

    except KeyboardInterrupt:
        print("Arrêt de l'application")
       