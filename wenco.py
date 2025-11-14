#!/usr/bin/env python
import os
import time

def banner():
    print("""
╔══════════════════════════════════════════════╗
║     🍪 ROBLOX COOKIE INJECTOR - WENCO       ║
║          Multi-Account Manager               ║
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
        input("Tekan Enter untuk keluar...")
        return
    
    print("[✓] Akses root tersedia.\n")
    
    # Daftar paket Roblox
    pkgs = [
        "com.mangcut.rulod",
        "com.mangcut.ruloe",
        "com.mangcut.rulof",
        "com.mangcut.rulog",
        "com.mangcut.ruloh",
        "com.mangcut.ruloi",
        "com.mangcut.ruloj",
        "com.mangcut.rulok",
    ]
    
    print("=" * 50)
    print("📱 PACKAGE ROBLOX YANG TERSEDIA:")
    print("=" * 50)
    for i, pkg in enumerate(pkgs, 1):
        print(f"   {i}. {pkg}")
    
    print("\n" + "=" * 50)
    
    # Input jumlah
    try:
        jumlah = int(input(f"\nBerapa package yang ingin dijalankan? (1-{len(pkgs)}): "))
        if jumlah < 1 or jumlah > len(pkgs):
            print(f"[✗] Masukkan angka antara 1-{len(pkgs)}!")
            return
    except ValueError:
        print("[✗] Input tidak valid!")
        return
    except KeyboardInterrupt:
        print("\n[!] Dibatalkan oleh user.")
        return
    
    selected_pkgs = pkgs[:jumlah]
    sql_path = "/sdcard/Download/inject.sql"
    
    print(f"\n[•] Akan menginjec {jumlah} package\n")
    print("=" * 50)
    
    # Loop untuk setiap package
    success_count = 0
    
    for i, pkg in enumerate(selected_pkgs, 1):
        print(f"\n[{i}/{jumlah}] 📱 Package: {pkg}")
        print("─" * 50)
        
        try:
            cookie = input(f"Masukkan cookie akun ke-{i}: ").strip()
        except KeyboardInterrupt:
            print("\n[!] Dibatalkan oleh user.")
            break
        
        if not cookie:
            print("[!] Cookie kosong, skip package ini.")
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
            print(f"    Pastikan package {pkg} sudah terinstall di device.")
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
        os.system(f"su -c 'monkey -p {pkg} -c android.intent.category.LAUNCHER 1' > /dev/null 2>&1")
        
        print(f"[✓] Selesai untuk {pkg}")
        success_count += 1
        
        # Delay sebelum package berikutnya
        if i < len(selected_pkgs):
            print("\n⏳ Menunggu 3 detik sebelum package berikutnya...")
            time.sleep(3)
    
    # Cleanup SQL file
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
    print("\n💡 Tips: Buka Roblox dan cek apakah sudah login\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[!] Program dibatalkan oleh user.")
    except Exception as e:
        print(f"\n[✗] Error tidak terduga: {e}")
