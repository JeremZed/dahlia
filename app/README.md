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



## Bugs

### Error

```sh
Traceback (most recent call last):
  File "....../app/main.py", line 2, in <module>
    from client.main import client_start
  File "....../app/client/main.py", line 2, in <module>
    from PyQt6.QtWebEngineWidgets import QWebEngineView
ImportError: .....miniconda3/envs/dahlia/bin/../lib/libstdc++.so.6: version GLIBCXX_3.4.30' not found (required by /lib/x86_64-linux-gnu/libLLVM.so.19.1)
```

### Solution

- Lister les versions actuelles:

```sh
strings $(g++ -print-file-name=libstdc++.so.6) | grep GLIBCXX
```

Si GLIBCXX_3.4.30 n'y est pas il faut mettre à jour libstdc++.

Suite à une mise à jour du système hôte, il faut forcer une mise à jour pour conda.

```sh
conda install -c conda-forge libstdcxx-ng
```