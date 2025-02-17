# Client Dahlia

## Architecture du Client Dahlia

Le Client Dahlia est structuré en deux composants principaux :

- Serveur Web (Backend) : Un serveur web basé sur FastAPI, fonctionnant en arrière-plan sur un thread dédié, gère la logique applicative et les communications.
- Interface Graphique (Frontend) : Une interface utilisateur graphique (GUI) constitue la partie client, permettant l'interaction avec le système.

## Install

### Fichier de configuration

Renommer le fichier .env.example en .env

### Installation des paquets python

```sh
pip install -r requierements.txt
```

## Générer un exécutable

```sh
pyinstaller --onefile --name dahlia main.py
```

## Générer les certificats SSL

```sh
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```