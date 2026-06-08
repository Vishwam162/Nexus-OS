import sys
import math
import os
import subprocess
from PyQt5.QtCore import QTimer, Qt, QRectF
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtGui import QPainter, QColor, QPen, QFont, QBrush

class DynamicNexusOS(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 1. Enforce Fullscreen Borderless Mode
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.SubWindow)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.showFullScreen()
        
        self.angle = 0.0
        
        # 2. Dynamic Cluster Registry
        # The system starts with your core presets, but WILL ADD MORE AUTOMATICALLY
        self.clusters = [
            {"name": "DEVELOPMENT TOOLS", "color": QColor(0, 255, 200), "apps": []},
            {"name": "COMMUNICATION", "color": QColor(255, 40, 70), "apps": []},
            {"name": "HACK LAB (KALI)", "color": QColor(150, 50, 255), "apps": []},
            {"name": "PRODUCTIVITY", "color": QColor(240, 200, 50), "apps": []}
        ]
        
        # 3. Scan and populate all pre-installed and newly downloaded tools automatically
        self.auto_scan_system_apps()
        
        # 4. Animation Frame Loop (~60 FPS)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_physics)
        self.timer.start(16)

    def auto_scan_system_apps(self):
        """Automatically scans Linux app registries and sorts them into spheres."""
        print("🔍 Nexus System Scanner searching for downloaded tools...")
        
        # In a fully built Linux OS, all downloaded apps drop a '.desktop' file here:
        app_dir = "/usr/share/applications/"
        
        # Fallback simulation list containing all your favorite platforms
        found_apps = ["vscode", "cursor", "github-desktop", "whatsapp-web", "teams", "gmail", "metasploit", "nmap", "thunar-filemanager", "google-sheets"]
        
        if os.path.exists(app_dir):
            try:
                # Real code to list files downloaded by apt or snap
                found_apps = [f.replace(".desktop", "") for f in os.listdir(app_dir) if f.endswith(".desktop")][:20]
            except Exception:
                pass

        # Automatically sort every single found app into its matching sphere
        for app in found_apps:
            self.sort_app_into_sphere_dynamic(app.upper())

    def sort_app_into_sphere_dynamic(self, app_name):
        """Logic to automatically place apps or create a new sphere if full."""
        # Rule: Max 3 apps per sphere to keep the design clean. If full, we make a new sphere!
        MAX_APPS_PER_SPHERE = 3
        
        # Smart keyword detection matching your requested tools
        target_category = "PRODUCTIVITY"
        if any(k in app_name for k in ["VSCODE", "CODE", "CURSOR", "GIT", "GITHUB"]):
            target_category = "DEVELOPMENT TOOLS"
        elif any(k in app_name for k in ["WHATSAPP", "TEAMS", "MESSENGER", "CHROME", "CHROMIUM"]):
            target_category = "COMMUNICATION"
        elif any(k in app_name for k in ["METASPLOIT", "NMAP", "WIRESHARK", "KALI", "TERMINAL"]):
            target_category = "HACK LAB (KALI)"

        # Find the correct sphere
        for cluster in self.clusters:
            if cluster["name"] == target_category:
                if len(cluster["apps"]) < MAX_APPS_PER_SPHERE:
                    cluster["apps"].append(app_name)
                    return
                
        # AUTOMATIC SPHERE SPARK LOGIC: If we reach here, it means the sphere is FULL.
        # It automatically creates a brand-new orbital cluster sphere on the fly!
        print(f"⚡ Sphere Full! Automatically generating new cluster for: {app_name}")
        new_sphere = {
            "name": f"EXPANDED {target_category}",
            "color": QColor(0, 150, 255),
            "apps": [app_name]
        }
        self.clusters.append(new_sphere)

    def update_physics(self):
        self.angle += 0.008 # Smooth rotation tracking speed
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        cx, cy = self.width() // 2, self.height() // 2
        
        # Deep Space Dark Wallpaper Matrix
        painter.setBrush(QBrush(QColor(5, 10, 18, 248)))
        painter.setPen(Qt.NoPen)
        painter.drawRect(0, 0, self.width(), self.height())
        
        # Central Nexus Core Hub
        hub_radius = 110
        painter.setBrush(Qt.NoBrush)
        painter.setPen(QPen(QColor(0, 240, 255, 220), 2))
        painter.drawEllipse(cx - hub_radius, cy - hub_radius, hub_radius * 2, hub_radius * 2)
        
        painter.setPen(QPen(QColor(255, 255, 255)))
        painter.setFont(QFont("Orbitron", 13, QFont.Bold))
        painter.drawText(QRectF(cx - 100, cy - 20, 200, 40), Qt.AlignCenter, "NEXUS COMMAND")
        
        # --- DYNAMIC GEOMETRY ENGINE ---
        # Instead of fixed 4, it divides the circle perfectly by the total number of clusters
        num_clusters = len(self.clusters)
        orbit_radius = 290
        
        painter.setPen(QPen(QColor(0, 240, 255, 20), 1))
        painter.drawEllipse(cx - orbit_radius, cy - orbit_radius, orbit_radius * 2, orbit_radius * 2)
        
        for i, cluster in enumerate(self.clusters):
            # Calculates the shifting angles dynamically based on how many spheres exist!
            current_angle = self.angle + (i * (2 * math.pi / num_clusters))
            ox = int(cx + orbit_radius * math.cos(current_angle))
            oy = int(cy + orbit_radius * math.sin(current_angle))
            
            # Vector connection string to central command
            painter.setPen(QPen(QColor(0, 240, 255, 40), 1))
            painter.drawLine(cx, cy, ox, oy)
            
            r = 60
            # Outer futuristic halo border
            painter.setPen(QPen(cluster["color"], 2))
            painter.setBrush(QBrush(QColor(10, 20, 32, 255)))
            painter.drawEllipse(ox - r, oy - r, r * 2, r * 2)
            
            # Display Sphere Category Title
            painter.setPen(QPen(QColor(255, 255, 255)))
            painter.setFont(QFont("Orbitron", 8, QFont.Bold))
            painter.drawText(QRectF(ox - 90, oy - r - 22, 180, 20), Qt.AlignCenter, cluster["name"])
            
            # Draw individual app items completely automatically inside the sphere
            painter.setFont(QFont("Arial", 8, QFont.Normal))
            painter.setPen(QPen(QColor(0, 240, 255, 220)))
            for idx, app_name in enumerate(cluster["apps"]):
                offset_y = (idx - len(cluster["apps"])/2) * 18
                painter.drawText(QRectF(ox - 55, oy + offset_y, 110, 16), Qt.AlignCenter, app_name[:12])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = DynamicNexusOS()
    sys.exit(app.exec_())