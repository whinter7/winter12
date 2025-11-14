#!/bin/bash

# ==========================================================
# Termux Setup Script (Fully Automatic & Error Tolerant)
# Dibuat untuk mengatasi masalah konflik konfigurasi (dpkg)
# ==========================================================

echo "Memulai proses instalasi Termux otomatis..."

# Variabel untuk mengatur non-interaktif
export DEBIAN_FRONTEND=noninteractive

# --- Fungsi untuk memeriksa status ---
check_status() {
    if [ $? -ne 0 ]; then
        echo -e "\n[!] ERROR: Perintah sebelumnya gagal. Menghentikan script."
        exit 1
    fi
}

# --- 1. Perbaikan dan Konfigurasi yang Gagal ---
echo -e "\n--- [1/4] Mencoba menyelesaikan konfigurasi paket yang gagal (dpkg) ---"
dpkg --configure -a

# --- 2. Update dan Upgrade Sistem (Non-Interaktif) ---
echo -e "\n--- [2/4] Melakukan pkg update dan upgrade (otomatis 'yes') ---"
pkg update -y
check_status

# Menggunakan DEBIAN_FRONTEND untuk menghindari prompt konflik konfigurasi (seperti bashrc)
pkg upgrade -y
check_status

# --- 3. Instalasi Paket yang Diminta ---
echo -e "\n--- [3/4] Memasang paket Python, SQLite, Coreutils, dan Busybox ---"
pkg install python sqlite coreutils busybox -y
check_status

# --- 4. Pembersihan Akhir ---
echo -e "\n--- [4/4] Membersihkan cache paket yang sudah tidak diperlukan ---"
pkg autoclean

# --- Selesai ---
echo -e "\n============================================="
echo "✅ Instalasi dan Pembaruan Termux Selesai!"
echo "============================================="
