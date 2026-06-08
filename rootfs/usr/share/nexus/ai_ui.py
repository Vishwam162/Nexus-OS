import sys
import requests
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLineEdit, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QColor, QPalette, QFont

class NexusAICard(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Translucent, Window-Bar Free Floating Block Architecture
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.resize(420, 600)
        
        # Center the panel to the right edge of the interface
        screen_geo = QApplication.desktop().screenGeometry()
        self.move(screen_geo.width() - 460, (screen_geo.height() - 600) // 2)

        # Main Layout Setup
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        layout.setContentsMargins(20, 20, 20, 20)

        # AI Header Title
        self.title_lbl = QLabel("🤖 NEXUS AI ASSISTANT (DeepSeek-R1)", self)
        self.title_lbl.setStyleSheet("color: #00f0ff; font-weight: bold; font-size: 14px;")
        layout.addWidget(self.title_lbl)

        # Chat Output Streams Workspace
        self.chat_display = QTextEdit(self)
        self.chat_display.setReadOnly(True)
        self.chat_display.setStyleSheet(
            "background-color: rgba(10, 18, 30, 220); color: #ffffff; "
            "border: 1px solid #00f0ff; border-radius: 8px; font-size: 12px; padding: 10px;"
        )
        self.chat_display.append("<font color='#00f0ff'>[System]:</font> Online. Neural connections initialized with local model mesh.")
        layout.addWidget(self.chat_display)

        # User Text Input Panel
        self.input_line = QLineEdit(self)
        self.input_line.setPlaceholderText("Transmit command string or system query...")
        self.input_line.setStyleSheet(
            "background-color: #122035; color: #ffffff; border: 1px solid #00aaff; "
            "border-radius: 6px; height: 35px; padding-left: 10px; font-size: 12px;"
        )
        self.input_line.returnPressed.connect(self.process_transmission)
        layout.addWidget(self.input_line)

    def process_transmission(self):
        user_text = self.input_line.text().strip()
        if not user_text:
            return
            
        self.chat_display.append(f"<br><font color='#e0a020'>[Vishwam]:</font> {user_text}")
        self.input_line.clear()
        QApplication.processEvents() # Clear display cache instantly
        
        # Connect to local Ollama core pipeline running DeepSeek-R1
        try:
            url = "http://127.0.0.1:11434/api/generate"
            payload = {"model": "deepseek-r1:3b", "prompt": user_text, "stream": False}
            res = requests.post(url, json=payload, timeout=10)
            ai_thought = res.json().get("response", "Transmission lost.")
            self.chat_display.append(f"<br><font color='#00f0ff'>[AI]:</font> {ai_thought}")
        except Exception:
            self.chat_display.append("<br><font color='#ff4040'>[Error]:</font> Unable to bridge to DeepSeek core node. Ensure Ollama is active.")

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.close() # Instantly closes the overlay window

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = NexusAICard()
    win.show()
    sys.exit(app.exec_())