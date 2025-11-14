#!/usr/bin/env python
import os
import shutil
import sys
import time

def banner():
    print("""
╔══════════════════════════════════════════════╗
║      🔧 TERMUX SETUP FOR ROBLOX INJECT      ║
╚══════════════════════════════════════════════╝
""")

def check_and_install(pkg):
    """Cek dan install package jika belum ada"""
    print(f"[•] Mengecek {pkg}...")
    if shutil.which(pkg) is None:
        print(f"[!] {pkg} belum terinstall. Menginstall...")
        result = os.system(f"pkg install -y {pkg}")
        if result != 0:
            print(f"[✗] Gagal menginstall {pkg}")
            return False
        print(f"[✓] {pkg} berhasil diinstall.")
    else:
        print(f"[✓] {pkg} sudah terinstall.")
    return True

def check_root():
    """Cek akses root"""
    print("\n[•] Mengecek akses root...")
    result = os.popen("su -c 'id' 2>/dev/null").read()
    if "uid=0" in result:
        print("[✓] Akses root tersedia.")
        return True
    else:
        print("[⚠] Akses root TIDAK tersedia!")
        print("    Device harus di-root untuk inject cookie.")
        return False

def check_storage():
    """Cek dan setup storage"""
    print("\n[•] Mengecek akses storage...")
    storage_path = os.path.expanduser("~/storage")
    if not os.path.exists(storage_path):
        print("[!] Storage belum diatur. Menjalankan setup...")
        os.system("termux-setup-storage")
        print("    ⚠ Berikan izin storage saat diminta!")
        time.sleep(3)
        if os.path.exists(storage_path):
            print("[✓] Akses storage berhasil diatur.")
        else:
            print("[⚠] Storage belum diatur. Silakan jalankan: termux-setup-storage")
    else:
        print("[✓] Akses storage sudah tersedia.")

def download_wenco():
    """Download wenco.py ke folder Download"""
    print("\n" + "="*50)
    print("📥 DOWNLOAD WENCO.PY")
    print("="*50)
    
    download_path = "/sdcard/Download/wenco.py"
    url = "https://raw.githubusercontent.com/whinter7/winter12/refs/heads/main/wenco.py"
    
    print(f"\n[•] Mendownload wenco.py...")
    print(f"[•] Dari: {url}")
    print(f"[•] Ke: {download_path}\n")
    
    # Coba dengan curl dulu
    result = os.system(f"curl -fsSL {url} -o {download_path} 2>/dev/null")
    
    # Kalau gagal, coba wget
    if result != 0:
        print("[!] Curl gagal, mencoba dengan wget...")
        result = os.system(f"wget -q {url} -O {download_path}")
    
    if result == 0 and os.path.exists(download_path):
        print("[✓] wenco.py berhasil didownload!")
        print(f"[✓] Lokasi: {download_path}")
        return True
    else:
        print("[✗] Gagal download wenco.py")
        return False

def run_wenco():
    """Jalankan wenco.py"""
    download_path = "/sdcard/Download/wenco.py"
    
    print("\n" + "="*50)
    print("🚀 MENJALANKAN WENCO.PY")
    print("="*50 + "\n")
    
    if not os.path.exists(download_path):
        print(f"[✗] File tidak ditemukan: {download_path}")
        return False
    
    print("[•] Memulai wenco.py...\n")
    time.sleep(1)
    
    # Jalankan wenco.py
    os.system(f"python {download_path}")
    return True

def main():
    banner()
    
    print("\n=== 📦 INSTALASI DEPENDENCIES ===\n")
    
    # Update package list
    print("[•] Memperbarui daftar package...")
    os.system("pkg update -y")
    print()
    
    # Install dependencies
    packages = ["python", "sqlite", "coreutils", "curl", "wget"]
    all_success = True
    
    for pkg in packages:
        if not check_and_install(pkg):
            all_success = False
    
    # Check root
    has_root = check_root()
    
    # Check storage
    check_storage()
    
    print("\n" + "="*50)
    
    if not all_success:
        print("[⚠] Beberapa package gagal diinstall.")
        print("    Periksa koneksi internet dan coba lagi.")
        sys.exit(1)
    
    if not has_root:
        print("\n[⚠] PERINGATAN: Device tidak memiliki akses root!")
        print("    Inject cookie tidak akan berfungsi tanpa root.")
        response = input("\nLanjutkan download wenco.py? (y/n): ").lower()
        if response != 'y':
            print("\n[•] Setup dibatalkan.")
            sys.exit(0)
    
    print("\n[✓] Setup Termux selesai!")
    
    # Download wenco.py
    if download_wenco():
        print("\n" + "="*50)
        response = input("\nJalankan wenco.py sekarang? (y/n): ").lower()
        
        if response == 'y':
            run_wenco()
        else:
            print("\n[•] Untuk menjalankan nanti, ketik:")
            print("    python /sdcard/Download/wenco.py")
    else:
        print("\n[✗] Setup selesai tapi wenco.py gagal didownload.")
        print("    Coba download manual atau cek koneksi internet.")
    
    print("\n" + "="*50)
    print("[✓] SETUP SELESAI!")
    print("="*50)
    print("\n📝 File wenco.py tersimpan di: /sdcard/Download/wenco.py")
    print("🔄 Untuk menjalankan lagi: python /sdcard/Download/wenco.py\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Setup dibatalkan oleh user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[✗] Error: {e}")
        sys.exit(1)
