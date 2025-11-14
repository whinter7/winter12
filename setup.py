#!/usr/bin/env python
import os
import shutil
import sys

def check_and_install(pkg):
    """Cek dan install package jika belum ada"""
    print(f"[•] Mengecek {pkg}...")
    if shutil.which(pkg) is None:
        print(f"[!] {pkg} belum terinstall. Menginstall...")
        result = os.system(f"pkg install -y {pkg}")
        if result != 0:
            print(f"[✗] Gagal menginstall {pkg}")
            return False
    else:
        print(f"[✓] {pkg} sudah terinstall.")
    return True

def check_su_access():
    """Cek akses root"""
    print("[•] Mengecek akses root...")
    result = os.popen("su -c 'id' 2>/dev/null").read()
    if "uid=0" in result:
        print("[✓] Akses root tersedia.")
        return True
    else:
        print("[✗] Akses root TIDAK tersedia.")
        print("    Pastikan device sudah di-root dan Termux punya izin su.")
        return False

def check_sqlite3():
    """Cek instalasi sqlite3"""
    print("[•] Mengecek sqlite3...")
    result = os.popen("sqlite3 --version 2>/dev/null").read()
    if result.strip():
        print(f"[✓] sqlite3 versi {result.strip()} tersedia.")
        return True
    else:
        print("[✗] sqlite3 tidak ditemukan.")
        print("    Coba install dengan: pkg install sqlite")
        return False

def check_python():
    """Cek instalasi Python"""
    print("[•] Mengecek Python...")
    version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"[✓] Python versi {version} tersedia.")
    return True

def check_termux_setup():
    """Cek apakah termux-setup-storage sudah dijalankan"""
    print("[•] Mengecek akses storage...")
    storage_path = os.path.expanduser("~/storage")
    if os.path.exists(storage_path):
        print("[✓] Akses storage sudah diatur.")
        return True
    else:
        print("[!] Storage belum diatur. Menjalankan termux-setup-storage...")
        os.system("termux-setup-storage")
        print("    Silakan berikan izin storage saat diminta.")
        return True

def main():
    print("=== 🔧 Setup & Validasi Termux untuk Inject Roblox Cookie ===\n")
    
    all_checks_passed = True
    
    # Update package list
    print("[•] Memperbarui daftar package...")
    os.system("pkg update -y")
    
    # Install dependencies
    packages = ["python", "sqlite", "coreutils", "busybox"]
    for pkg in packages:
        if not check_and_install(pkg):
            all_checks_passed = False
    
    print()
    
    # Check termux storage
    check_termux_setup()
    
    # Check root access
    if not check_su_access():
        all_checks_passed = False
        print("\n[!] PERINGATAN: Tanpa akses root, script inject mungkin tidak berfungsi!")
    
    # Verify installations
    print()
    check_sqlite3()
    check_python()
    
    print("\n" + "="*60)
    if all_checks_passed:
        print("[✓] Setup selesai! Semua komponen siap digunakan.")
        print("\nLangkah selanjutnya:")
        print("1. Pastikan Roblox sudah terinstall di device")
        print("2. Siapkan cookie Roblox yang valid")
        print("3. Jalankan script inject cookie")
    else:
        print("[✗] Setup selesai dengan beberapa masalah.")
        print("    Periksa error di atas dan perbaiki sebelum melanjutkan.")
    print("="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Setup dibatalkan oleh user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n[✗] Error tidak terduga: {e}")
        sys.exit(1)
