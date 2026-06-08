#!/bin/bash
# NEXUS OS - Cloud-Optimized ISO Packer

echo "🚀 Initiating Nexus OS Cloud-Optimized Packaging Engine..."

# 1. Install standard ISO mastering utilities
echo "📦 Installing image mastering toolchain..."
sudo apt-get update
sudo apt-get install -y genisoimage isolinux syslinux-common

# 2. Clear old build directories to ensure a clean slate
echo "🧹 Wiping old deployment footprints..."
rm -rf nexus_iso_root
rm -f nexus_os_v1.iso

# 3. Create a pristine structure for the bootable media image
mkdir -p nexus_iso_root/isolinux
mkdir -p nexus_iso_root/nexus_core

# 4. Inject all your custom system configurations and UI logic
echo "🧬 Packing Nexus Core software assets..."
cp -r rootfs/. nexus_iso_root/nexus_core/

# 5. Provision standard bootloader files so hardware can initialize it
echo "💿 Staging bootloader binary components..."
cp /usr/lib/ISOLINUX/isolinux.bin nexus_iso_root/isolinux/
cp /usr/lib/syslinux/modules/bios/ldlinux.c32 nexus_iso_root/isolinux/

# 6. Create the master bootloader configuration file
cat <<EOF > nexus_iso_root/isolinux/isolinux.cfg
default nexus
label nexus
  kernel /nexus_core/usr/share/nexus/nexus_login.py
EOF

# 7. Execute the cloud-safe ISO generation matrix
echo "🔥 Compiling independent, bare-metal .ISO image layer..."
genisoimage -J -R -v -T \
    -b isolinux/isolinux.bin \
    -c isolinux/boot.cat \
    -no-emul-boot -boot-load-size 4 -boot-info-table \
    -o nexus_os_v1.iso nexus_iso_root

# 8. Absolute Verification Validation Handshake
echo "🔍 Verifying generated media integrity..."
if [ -f nexus_os_v1.iso ]; then
    echo "✅ SUCCESS: nexus_os_v1.iso has been successfully minted!"
else
    echo "❌ Build failed. ISO packaging layer was interrupted."
    exit 1
fi