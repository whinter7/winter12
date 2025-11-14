#!/bin/bash

# ==========================================================
# Termux Setup Script - Revisi Akhir (Otomatis & Stabil)
# Fungsi: Update, Upgrade, Perbaikan Error, dan Instalasi Paket
# ==========================================================

echo "Memulai proses instalasi Termux otomatis dan tangguh..."

# Mengatur lingkungan ke non-interaktif untuk menghindari prompt konflik konfigurasi
export DEBIAN_FRONTEND=noninteractive

# --- Fungsi untuk memeriksa status dan keluar jika gagal ---
check_status() {
    if [ $? -ne 0 ]; then
        echo -e "\n[!] ERROR: Perintah sebelumnya gagal (Kode Keluar: $?). Menghentikan script."
        # Menonaktifkan non-interaktif saat keluar, untuk jaga-jaga
        unset DEBIAN_FRONTEND
        exit 1
    fi
}

# --- 1. Perbaikan dan Konfigurasi yang Gagal ---
echo -e "\n--- [1/5] Mencoba menyelesaikan konfigurasi paket yang gagal (dpkg --configure -a) ---"
dpkg --configure -a

# --- 2. Update Sistem ---
echo -e "\n--- [2/5] Melakukan pkg update ---"
pkg update -y
check_status

# --- 3. Upgrade Sistem ---
echo -e "\n--- [3/5] Melakukan pkg upgrade (Non-Interaktif) ---"
pkg upgrade -y
check_status

# --- 4. Instalasi Paket yang Diminta ---
echo -e "\n--- [4/5] Memasang paket Python, SQLite, Coreutils, dan Busybox ---"
pkg install python sqlite coreutils busybox -y
check_status

# --- 5. Pembersihan dan Verifikasi ---
echo -e "\n--- [5/5] Membersihkan cache paket yang sudah tidak diperlukan ---"
pkg autoclean

# Menonaktifkan non-interaktif setelah selesai
unset DEBIAN_FRONTEND

echo -e "\n============================================="
echo "✅ Instalasi dan Pembaruan Termux Selesai!"
echo "Semua paket sudah terinstal."
echo "============================================="
