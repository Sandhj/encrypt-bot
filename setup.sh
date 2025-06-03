#!/bin/bash

# Buat direktori proyek

mkdir -p /opt/encrypt
cd /opt/encrypt

# Buat venv untuk Bot
# Fungsi untuk deteksi OS dan versi
OS=$(grep -Ei '^(NAME|VERSION_ID)=' /etc/os-release | cut -d= -f2 | tr -d '"')

# Ekstrak nama distro dan versi
DISTRO=$(echo "$OS" | head -n1)
VERSION=$(echo "$OS" | tail -n1)

# Cek apakah Debian 12
if [[ "$DISTRO" == "Debian GNU/Linux" && "$VERSION" == "12" ]]; then
    echo "OS Terdeteksi: Debian 12"
    apt update && apt install python3.11-venv -y

# Cek apakah Ubuntu 24.04 LTS
elif [[ "$DISTRO" == "Ubuntu" && "$VERSION" == "24.04" ]]; then
    echo "OS Terdeteksi: Ubuntu 24.04 LTS"
    apt update && apt install python3.12-venv -y

# Jika bukan salah satu dari di atas
else
    echo "OS Tidak Didukung!"
    echo "Distro: $DISTRO"
    echo "Versi: $VERSION"
    exit 1
fi


python3 -m venv bot
source bot/bin/activate

apt-get install -y python3-pip

# Instal modul Python yang diperlukan
pip3 install requests
pip3 install schedule
pip3 install pyTelegramBotAPI

wget -q https://raw.githubusercontent.com/Sandhj/encrypt-bot/main/encrypt.sh
