from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebEngineCore import QWebEngineProfile, QWebEnginePage
from PyQt6.QtNetwork import QSslConfiguration, QSslCertificate, QSslKey, QSsl, QSslSocket
from PyQt6.QtCore import QUrl, QByteArray
import sys, os
from dotenv import load_dotenv

def on_cert_error(e):
    """
        Acceptation du certification SSL autosigné uniquement pour DEV
    """
    print(f"cert error: {e.description()}")
    print(f"type: {e.type()}")
    print(f"overridable: {e.isOverridable()}")
    print(f"url: {e.url()}")
    for c in e.certificateChain():
        print(c.toText())

    if os.getenv('ENV') == 'DEV':
        e.acceptCertificate()

def load_from_file(path):
    """
        Permet de récupérer le contenu de la clé privé SSH
    """
    with open(path, 'rb') as f:
        key_data = f.read()
    return QByteArray(key_data)


def setup_ssl():
    """
        Permet de gérer la connexion SSL au serveur FastAPI via le client Qt
    """

    # Chargement du certificat
    cert_data = load_from_file( os.path.join(os.path.dirname(__file__), '../certs/cert.pem') )
    cert = QSslCertificate(cert_data)

    # Ajout du certificat et la clé
    ssl_config = QSslConfiguration.defaultConfiguration()

    ssl_config.addCaCertificate(cert)

    # ssl_config.setPeerVerifyMode(QSslSocket.PeerVerifyMode.VerifyNone)

    # Applique la configuration SSL par défaut
    QSslConfiguration.setDefaultConfiguration(ssl_config)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle(f"{os.getenv('APP_TITLE')}")
        self.setGeometry(
            int(os.getenv('APP_POSITION_X')),
            int(os.getenv('APP_POSITION_Y')),
            int(os.getenv('APP_SIZE_W')),
            int(os.getenv('APP_SIZE_H'))
        )

        profile = QWebEngineProfile.defaultProfile()
        profile.setHttpCacheType(QWebEngineProfile.HttpCacheType.NoCache)


        self.browser = QWebEngineView()

        self.browser.page().certificateError.connect(on_cert_error)

        protocol = 'http'
        if os.getenv('FASTAPI_SSL_ENABLED') == 'true':
            protocol = 'https'

        url = f"{protocol}://{os.getenv('FASTAPI_IP')}:{os.getenv('FASTAPI_PORT')}"

        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)

def client_start():

    load_dotenv()

    app = QApplication(sys.argv)

    # Configurer SSL
    if os.getenv('FASTAPI_SSL_ENABLED') == 'true':
        setup_ssl()

    window = MainWindow()
    window.show()
    sys.exit(app.exec())
