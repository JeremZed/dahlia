# INSTALL

## Environnement de développement

### Installation des paquets

```sh
    sudo apt-get update && sudo apt install python3-pyqt5 python3-pyqt5.qtwebengine
```

### Création de l'environnement python

```sh
conda create -n dahlia python=3.12
conda activate dahlia

pip install -r app/requierements.txt
```

### Création de la variable d'environnement

```sh
cp app/.env.example app/.env
```

### Génération des certificats SSL

```sh
mkdir app/certs
openssl req -x509 -newkey rsa:4096 -keyout app/certs/key.pem -out app/certs/cert.pem -days 365 -nodes
```