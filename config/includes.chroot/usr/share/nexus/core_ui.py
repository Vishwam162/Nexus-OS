import sys
import math
import subprocess
from PyQt5.QtCore import QTimer, Qt, QPoint, QRectF
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QBrush

class NexusOSDesktop(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Force Fullscreen Borderless Mode (Bypasses traditional Desktop Windows)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showFullScreen()
        
        # 2. UI Physics & Animation Parameters
        self.angle = 0.0
        self.zoom_factors = [1.0, 1.0, 1.0, 1.0] # Scale tracking for the 4 clusters
        self.target_zooms = [1.0, 1.0, 1.0, 1.0]
        
        # 3. Define the Futuristic Clusters from your Blueprint
        self.clusters = [
            {"name": "DEV CORE", "color": QColor(0, 255, 150), "cmd": "code ."},
            {"name": "HACK LAB", "color": QColor(255, 50, 50), "cmd": "qterminal"},
            {"name": "CREATIVE", "color": QColor(200, 50, 255), "cmd": "gimp"},
            {"name": "MATRIX AI", "color": QColor(0, 200, 255), "cmd": "echo 'AI Summoned'"}
        ]
        
        # 4. Refresh Loop (60 FPS Animation Engine Matrix)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_physics)
        self.timer.start(16) # ~60 FPS (1000ms / 16ms)

    def update_physics(self):
        """Calculates rotational vector geometry and spring animations."""
        self.angle += 0.015 # Rotation step speed
        
        # Smooth interpolation (lerp) for the zooming/spreading animation scale
        for i in range(4):
            self.zoom_factors[i] += (self.target_zooms[i] - self.zoom_factors[i]) * 0.15
            
        self.update() # Triggers repaint handler

    def paintEvent(self, event):
        """The Master Rendering Matrix. Handles custom graphics pipeline directly."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Fetch resolution metrics dynamically
        width = self.width()
        height = self.height()
        cx, cy = width // 2, height // 2
        
        # --- LAYER 1: Futuristic Deep Background Shadow ---
        painter.setBrush(QBrush(QColor(5, 12, 22, 240)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, width, height)
        
        # --- LAYER 2: Central Nexus Command Hub Ring ---
        hub_radius = 110
        painter.setBrush(Qt.NoBrush)
        pen = QPen(QColor(0, 220, 255, 180), 3)
        painter.setPen(pen)
        painter.drawEllipse(cx - hub_radius, cy - hub_radius, hub_radius * 2, hub_radius * 2)
        
        # Outer dotted alignment ticks
        pen.setStyle(Qt.DashLine)
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawEllipse(cx - (hub_radius + 15), cy - (hub_radius + 15), (hub_radius + 15) * 2, (hub_radius + 15) * 2)
        
        # Core Text Rendering
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Arial", 14, QFont.Bold))
        painter.drawText(QRectF(cx - 100, cy - 20, 200, 40), Qt.AlignCenter, "NEXUS CENTRAL")
        
        # --- LAYER 3: Orbital Processing Array ---
        orbit_radius = 240
        
        for i, cluster in enumerate(self.clusters):
            # Mathematical calculation for splitting 4 elements perfectly over 360 degrees
            current_angle = self.angle + (i * (math.pi / 2))
            
            # Translate polar coordinates to window X/Y coordinates
            ox = int(cx + orbit_radius * math.cos(current_angle))
            oy = int(cy + orbit_radius * math.sin(current_angle))
            
            # Draw network line back to core
            painter.setPen(QPen(QColor(0, 220, 255, 60), 1))
            painter.drawLine(cx, cy, ox, oy)
            
            # Fetch animation scale factor
            scale = self.zoom_factors[i]
            sphere_radius = int(35 * scale)
            
            # Draw Orbital Interactive Nodes
            painter.setBrush(QBrush(cluster["color"]))
            painter.setPen(QPen(QColor(255, 255, 255, 200), 2))
            painter.drawEllipse(ox - sphere_radius, oy - sphere_radius, sphere_radius * 2, sphere_radius * 2)
            
            # Label Clusters
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            painter.drawText(QRectF(ox - 80, oy + sphere_radius + 5, 160, 20), Qt.AlignCenter, cluster["name"])

    def mousePressEvent(self, event):
        """Interprets spatial touch/clicks to trigger expanding app execution mechanics."""
        cx, cy = self.width() // 2, self.height() // 2
        orbit_radius = 240
        
        for i, cluster in enumerate(self.clusters):
            current_angle = self.angle + (i * (math.pi / 2))
            ox = int(cx + orbit_radius * math.cos(current_angle))
            oy = int(cy + orbit_radius * math.sin(current_angle))
            
            # Use distance formula to verify if click hit the orbiter boundaries
            distance = math.sqrt((event.x() - ox)**2 + (event.y() - oy)**2)
            if distance <= 40:
                print(f"🔥 Nexus Sector Triggered: {cluster['name']}")
                # Fire the zoom-out/expanding scale pop visual physics effect
                self.target_zooms[i] = 2.5
                QTimer.singleShot(300, lambda idx=i: self.reset_zoom(idx))
                
                # Execute underlying tool natively in OS workspace
                try:
                    subprocess.Popen(cluster["cmd"], shell=True)
                except Exception as e:
                    print(f"Execution handling failure: {e}")
                break

    def reset_zoom(self, index):
        """Returns the cluster back to standard rotation parameters."""
        self.target_zooms[index] = 1.0

if __name__ == "__main__":
    # Core system runtime loop
    app = QApplication(sys.argv)
    desktop = NexusOSDesktop()
    sys.exit(app.exec_())