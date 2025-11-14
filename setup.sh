#!/bin/bash

# ===============================================
# Termux Package Setup Script (Enhanced)
# ===============================================

echo "Memulai proses pembaruan dan instalasi paket Termux..."

# Fungsi untuk memeriksa status perintah dan keluar jika gagal
check_status() {
    if [ $? -ne 0 ]; then
        echo -e "\n[!] ERROR: Perintah sebelumnya gagal. Menghentikan script."
        exit 1
    fi
}

# 1. Update list paket
echo -e "\n--- [1/4] Melakukan pkg update ---"
pkg update
check_status

# 2. Tangani konfigurasi paket yang tertunda (misalnya error 'apt' atau 'dpkg')
echo -e "\n--- [2/4] Mencoba menyelesaikan konfigurasi paket yang gagal (dpkg) ---"
dpkg --configure -a

# 3. Upgrade paket yang sudah terinstal
# Menggunakan '|| true' agar script tidak langsung gagal jika upgrade memerlukan input,
# tetapi juga akan dijalankan ulang (seperti di bawah).
echo -e "\n--- [3/4] Melakukan pkg upgrade dengan -y (otomatis 'yes') ---"
pkg upgrade -y

# Jalankan update dan upgrade lagi untuk memastikan semua dependensi terinstal dengan baik
# dan untuk menyelesaikan prompt yang mungkin terlewat.
echo -e "\n--- Mengulang update dan upgrade untuk memastikan konsistensi sistem ---"
pkg update && pkg upgrade -y
check_status

# 4. Instalasi paket yang diminta
echo -e "\n--- [4/4] Memasang paket Python, SQLite, Coreutils, dan Busybox ---"
pkg install python sqlite coreutils busybox -y
check_status

echo -e "\n============================================="
echo "✅ Instalasi dan Pembaruan Termux Selesai!"
echo "Semua paket yang diminta telah diinstal."
echo "============================================="
