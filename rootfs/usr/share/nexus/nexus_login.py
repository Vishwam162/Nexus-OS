import sys
import subprocess
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QVBoxLayout, QWidget, QLabel
from PyQt5.QtGui import QColor, QFont

class NexusSecurityGate(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Enforce Lockdown Screen Mode
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.showFullScreen()
        
        widget = QWidget(self)
        self.setCentralWidget(widget)
        layout = QVBoxLayout(widget)
        layout.setAlignment(Qt.AlignCenter)
        
        # System Identity Display
        self.lock_title = QLabel("NEXUS OS v1.0", self)
        self.lock_title.setStyleSheet("color: #00f0ff; font-size: 28px; font-weight: bold; margin-bottom: 10px;")
        layout.addWidget(self.lock_title)
        
        self.sub_title = QLabel("ACCESS RESTRICTED - KEY IN AUTHORIZATION MATRIX", self)
        self.sub_title.setStyleSheet("color: #80a0c0; font-size: 11px; margin-bottom: 30px;")
        layout.addWidget(self.sub_title)
        
        # Password Protection Entry Node
        self.pass_field = QLineEdit(self)
        self.pass_field.setEchoMode(QLineEdit.Password)
        self.pass_field.setPlaceholderText("Enter System Passphrase...")
        self.pass_field.setStyleSheet(
            "background-color: #0c1423; color: #ffffff; border: 2px solid #00f0ff; "
            "border-radius: 6px; width: 300px; height: 40px; font-size: 16px; text-align: center;"
        )
        self.pass_field.returnPressed.connect(self.verify_clearance)
        layout.addWidget(self.pass_field)
        
        self.status_lbl = QLabel("", self)
        self.status_lbl.setStyleSheet("color: #ff4040; margin-top: 15px; font-weight: bold;")
        layout.addWidget(self.status_lbl)

    def verify_clearance(self):
        # We will hardcode your password choice securely right here
        if self.pass_field.text() == "nexus2026":
            self.status_lbl.setStyleSheet("color: #00ffaa;")
            self.status_lbl.setText("ACCESS GRANTED. INITIALIZING CORE DESKTOP COMPOSITOR...")
            QApplication.processEvents()
            
            # Start the main desktop interface system script natively
            subprocess.Popen(["python3", "/usr/share/nexus/core_ui.py"])
            self.close()
        else:
            self.status_lbl.setText("AUTHENTICATION FAIL: ACCESS SIGNATURE INVALID.")
            self.pass_field.clear()

    def paintEvent(self, event):
        # Dark secure system backdrop fill
        painter = QPainter(self)
        painter.fillRect(0, 0, self.width(), self.height(), QColor(5, 8, 15))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    gate = NexusSecurityGate()
    gate.show()
    sys.exit(app.exec_())