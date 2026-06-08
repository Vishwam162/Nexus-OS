#!/bin/bash
# NEXUS OS - Master Compiler Script (Cross-Build Fix)

echo "🚀 Initiating Nexus OS Compilation Matrix..."

# 1. Prepare Ubuntu Cloud Environment
echo "🌐 Ensuring repositories are active..."
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo add-apt-repository -y universe
sudo apt-get update

# 2. Install live-build AND the Debian security keys
echo "📦 Installing live-build toolchain and Debian keyrings..."
sudo apt-get install -y live-build xorriso squashfs-tools debian-archive-keyring

# 3. Clean up broken files
echo "🧹 Wiping old build data..."
sudo lb clean

# 4. Configure Linux Base Engine - FORCING explicit Debian Mirrors!
echo "⚙️ Configuring Linux Base Engine..."
lb config -d bookworm \
  --mirror-bootstrap "http://deb.debian.org/debian/" \
  --mirror-chroot "http://deb.debian.org/debian/" \
  --mirror-binary "http://deb.debian.org/debian/" \
  --archive-areas "main contrib non-free non-free-firmware" \
  --binary-images iso-hybrid

# 5. Define the pre-installed tools
echo "📦 Staging Nexus packages..."
mkdir -p config/package-lists
cat <<EOF > config/package-lists/nexus.list.chroot
# Core Boot & Graphics Engine
live-boot
live-config
systemd
xserver-xorg
xinit
wayland-protocols

# Python & AI UI Dependencies
python3
python3-pip
python3-pyqt5
python3-requests

# Global App Suite (Your Requested Branded & Core Tools)
chromium             # Handles Gmail, Google Tools, WhatsApp, Teams, and Web Browsing
thunar               # Your futuristic, custom-styled File Explorer
git                  # Deep integration for GitHub version control
curl                 # Needed for pulling developer repository keys
wget                 # Web downloader utility
nano                 # Fast terminal text editor
htop                 # System performance monitoring dashboard
EOF

# 6. Safely inject your custom system files
echo "🧬 Injecting Nexus UI and AI Daemon into the core..."
mkdir -p config/includes.chroot/
cp -r rootfs/. config/includes.chroot/

# 7. Force the OS to boot into YOUR interface on startup
echo "🔒 Writing boot sequence override..."
mkdir -p config/hooks/normal
cat <<EOF > config/hooks/normal/01-enable-nexus-service.hook.chroot
#!/bin/sh
systemctl enable nexus-ui.service
EOF
chmod +x config/hooks/normal/01-enable-nexus-service.hook.chroot

# 8. Compile the Final ISO
echo "🔥 Compiling bare-metal .ISO file. Please hold..."
sudo lb build

# 9. Verify and Rename Output
if [ -f live-image-amd64.hybrid.iso ]; then
    mv live-image-amd64.hybrid.iso nexus_os_v1.iso
    echo "✅ SUCCESS: nexus_os_v1.iso is ready for launch!"
else
    echo "❌ Build failed. Check the errors above."
fi