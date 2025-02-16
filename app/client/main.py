from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile, QWebEnginePage
from PyQt5.QtCore import QUrl
import sys, os
from dotenv import load_dotenv

class CustomWebEnginePage(QWebEnginePage):
    """
        Class perso pour gérer le profile utilisé dans le QWebEngineView
    """
    def __init__(self, profile, parent=None):
        super().__init__(parent)
        self.profile = profile

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
        profile.setHttpCacheType(QWebEngineProfile.NoCache)

        self.browser = QWebEngineView()

        page = CustomWebEnginePage(profile, self.browser)
        self.browser.setPage(page)

        url = f"{os.getenv('FASTAPI_PROTOCOL')}://{os.getenv('FASTAPI_IP')}:{os.getenv('FASTAPI_PORT')}"
        
        self.browser.setUrl(QUrl(url))
        self.setCentralWidget(self.browser)

def client_start():
    
    load_dotenv()

    qt_app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(qt_app.exec_())
