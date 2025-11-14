#!/bin/bash

echo "Memulai pembaruan dan instalasi paket Termux..."

# 1. Update list paket
echo -e "\n--- Melakukan pkg update ---"
pkg update

# 2. Upgrade paket yang sudah terinstal
echo -e "\n--- Melakukan pkg upgrade ---"
pkg upgrade -y # Opsi -y agar otomatis menjawab 'yes' pada pertanyaan konfirmasi

# 3. Instalasi paket yang diminta
echo -e "\n--- Memasang paket Python, SQLite, Coreutils, dan Busybox ---"
pkg install python sqlite coreutils busybox -y

echo -e "\n--- Instalasi selesai! ---"
echo "Semua paket yang diminta (python, sqlite, coreutils, busybox) telah diinstal."
