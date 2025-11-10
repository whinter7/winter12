#!/bin/bash

echo "[*] Memulai setup environment Termux untuk automasi Roblox..."
cd $HOME

# 🔄 Bersihkan storage lama jika ada
if [ -e "$HOME/storage" ]; then
    echo "[*] Menghapus storage lama..."
    rm -rf "$HOME/storage"
fi

# 📂 Setup akses storage
termux-setup-storage

# 🔄 Update dan upgrade package
yes | pkg update
yes | pkg upgrade

# 🔁 Ganti repository agar lebih stabil (opsional)
curl -s https://raw.githubusercontent.com/u400822/setup-termux/refs/heads/main/termux-change-repo.sh | bash

# 🐍 Install Python dan pip
yes | pkg install python
yes | pkg install python-pip

# 📦 Install library Python untuk automasi login
pip install --upgrade pip
pip install requests asyncio pyjwt prettytable pycryptodome psutil

# 📥 Unduh skrip Python login Roblox dari GitHub kamu
curl -Ls "https://raw.githubusercontent.com/USERNAME/REPO/BRANCH/login_roblox.py" -o /sdcard/Download/login_roblox.py

echo "[✓] Setup selesai. Skrip Python disimpan di /sdcard/Download/login_roblox.py"
