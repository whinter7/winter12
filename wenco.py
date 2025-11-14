#!/usr/bin/env python
import os
import time
import sys

# --- Helper Functions for Robust Input ---

def get_valid_int_input(prompt, min_val, max_val):
    """Meminta input integer yang valid dalam rentang tertentu."""
    while True:
        try:
            # Menggunakan sys.stdin.fileno() untuk cek interaktif
            # Walaupun ini lebih advanced, kita fokus pada penanganan errornya.
            
            # Mencegah EOFError saat input di-redirect atau dibatalkan
            user_input = input(prompt).strip()
            
            if not user_input:
                print("[!] Input kosong. Silakan masukkan angka.")
                continue

            jumlah = int(user_input)
            if jumlah < min_val or jumlah > max_val:
                print(f"[✗] Masukkan angka antara {min_val}-{max_val}!")
                continue
            return jumlah
            
        except EOFError:
            print("\n[✗] Error: EOF saat membaca baris. Pastikan Anda menjalankan skrip secara interaktif!")
            sys.exit(1)
        except ValueError:
            print("[✗] Input tidak valid! Silakan masukkan angka.")
        except KeyboardInterrupt:
            raise # Biarkan KeyboardInterrupt ditangani oleh blok utama

def get_cookie_input(prompt):
    """Meminta input cookie dan memastikan tidak kosong."""
    while True:
        try:
            cookie = input(prompt).strip()
            if not cookie:
                choice = input("[!] Cookie kosong. Lanjut tanpa cookie untuk package ini? (y/n): ").lower()
                if choice == 'y':
                    return None
                else:
                    continue
            return cookie
        except EOFError:
            print("\n[✗] Error: EOF saat membaca baris. Pastikan Anda menjalankan skrip secara interaktif!")
            sys.exit(1)
        except KeyboardInterrupt:
            raise # Biarkan KeyboardInterrupt ditangani oleh blok utama

# --- Original Functions ---

def banner():
    print("""
╔══════════════════════════════════════════════╗
║     🍪 ROBLOX COOKIE INJECTOR - WENCO         ║
║            Multi-Account Manager             ║
╚══════════════════════════════════════════════╝
""")

def check_root():
    """Cek akses root"""
    result = os.popen("su -c 'id' 2>/dev/null").read()
    if "uid=0" not in result:
        print("[✗] ERROR: Akses root tidak tersedia!")
        print("    Device harus di-root untuk menggunakan tool ini.\n")
        return False
    return True

def main():
    banner()
    
    # Check root dulu
    if not check_root():
        # Mengganti input() dengan sys.stdin.read(1) untuk menghindari EOFError di beberapa lingkungan
        # Namun, kita tetap menggunakan input() yang lebih user-friendly.
        try:
            input("Tekan Enter untuk keluar...")
        except:
            pass
        return
    
    print("[✓] Akses root tersedia.\n")
    
    # Daftar paket Roblox
    pkgs = [
        "com.mangcut.rulod", "com.mangcut.ruloe", "com.mangcut.rulof",
        "com.mangcut.rulog", "com.mangcut.ruloh", "com.mangcut.ruloi",
        "com.mangcut.ruloj", "com.mangcut.rulok",
    ]
    
    print("=" * 50)
    print("📱 PACKAGE ROBLOX YANG TERSEDIA:")
    print("=" * 50)
    for i, pkg in enumerate(pkgs, 1):
        print(f"    {i}. {pkg}")
    
    print("\n" + "=" * 50)
    
    # Input jumlah (menggunakan fungsi helper)
    jumlah = get_valid_int_input(
        f"\nBerapa package yang ingin dijalankan? (1-{len(pkgs)}): ", 
        1, len(pkgs)
    )
    
    selected_pkgs = pkgs[:jumlah]
    sql_path = "/sdcard/Download/inject.sql"
    
    print(f"\n[•] Akan menginjec {jumlah} package\n")
    print("=" * 50)
    
    # Loop untuk setiap package
    success_count = 0
    
    for i, pkg in enumerate(selected_pkgs, 1):
        print(f"\n[{i}/{jumlah}] 📱 Package: {pkg}")
        print("─" * 50)
        
        # Input cookie (menggunakan fungsi helper)
        cookie = get_cookie_input(f"Masukkan cookie akun ke-{i}: ")
        
        if cookie is None:
            print("[!] Skip package ini (cookie kosong).")
            continue
        
        db_path = f"/data/data/{pkg}/app_webview/Default/Cookies"
        
        # Buat SQL inject
        sql = f"""
DELETE FROM cookies WHERE host_key = '.roblox.com' AND name = '.ROBLOSECURITY';

INSERT INTO cookies (
    creation_utc, top_frame_site_key, host_key, name, value, encrypted_value,
    path, expires_utc, is_secure, is_httponly, last_access_utc,
    has_expires, is_persistent, priority, samesite,
    source_scheme, source_port, is_same_party
)
VALUES (
    13200000000000000, '', '.roblox.com', '.ROBLOSECURITY', '{cookie}', '',
    '/', 99999999999999999, 1, 1, 13200000000000000,
    1, 1, 1, -1, 0, -1, 0
);
"""
        
        # Simpan SQL ke file
        try:
            with open(sql_path, "w") as f:
                f.write(sql)
            print(f"[✓] SQL file dibuat")
        except Exception as e:
            print(f"[✗] Gagal membuat SQL file: {e}")
            continue
        
        # Inject ke database
        print(f"[•] Menginjec cookie...")
        result = os.system(f"su -c 'sqlite3 {db_path} < {sql_path}' 2>/dev/null")
        
        if result != 0:
            print(f"[✗] Gagal inject cookie!")
            print(f"    Pastikan package {pkg} sudah terinstall di device DAN device sudah root.")
            # Hapus file SQL jika gagal (untuk keamanan)
            if os.path.exists(sql_path):
                os.remove(sql_path)
            continue
        
        # Set permission read-only
        os.system(f"su -c 'chmod 444 {db_path}' 2>/dev/null")
        print(f"[✓] Cookie berhasil diinjec")
        
        # Force stop app
        print(f"[•] Menutup aplikasi...")
        os.system(f"su -c 'am force-stop {pkg}' 2>/dev/null")
        time.sleep(1)
        
        # Buka app
        print(f"[•] Membuka aplikasi...")
        # Hanya jalankan jika diperlukan, atau tinggalkan saja agar user buka manual
        # os.system(f"su -c 'monkey -p {pkg} -c android.intent.category.LAUNCHER 1' > /dev/null 2>&1")
        
        print(f"[✓] Selesai untuk {pkg}")
        success_count += 1
        
        # Delay sebelum package berikutnya
        if i < len(selected_pkgs):
            print("\n⏳ Menunggu 3 detik sebelum package berikutnya...")
            time.sleep(3)
    
    # Cleanup SQL file (dipastikan sudah dihapus dalam loop, tapi ini sebagai fallback)
    try:
        if os.path.exists(sql_path):
            os.remove(sql_path)
    except:
        pass
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 SUMMARY")
    print("=" * 50)
    print(f"✓ Berhasil: {success_count}/{jumlah}")
    print(f"✗ Gagal   : {jumlah - success_count}/{jumlah}")
    print("=" * 50)
    print("\n[✓] Proses selesai!")
    print("\n💡 Tips: Buka aplikasi Roblox secara manual dan cek apakah sudah login\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program dibatalkan oleh user.")
        sys.exit(0)
    except Exception as e:
        # Menambahkan pengecekan untuk EOFError yang mungkin terlewat
        if isinstance(e, EOFError):
             print("\n[✗] Error: EOF saat membaca baris. Pastikan Anda menjalankan skrip secara interaktif!")
        else:
             print(f"\n[✗] Error tidak terduga: {e}")
        sys.exit(1)
