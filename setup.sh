import os
import shutil

def check_and_install(pkg):
    print(f"[•] Mengecek {pkg}...")
    if shutil.which(pkg) is None:
        print(f"[!] {pkg} belum terinstall. Menginstall...")
        os.system(f"pkg install -y {pkg}")
    else:
        print(f"[✓] {pkg} sudah terinstall.")

def check_su_access():
    print("[•] Mengecek akses root...")
    result = os.popen("su -c 'id'").read()
    if "uid=0" in result:
        print("[✓] Akses root tersedia.")
    else:
        print("[✗] Akses root TIDAK tersedia. Pastikan device sudah di-root dan Termux punya izin.")

def check_sqlite3():
    print("[•] Mengecek sqlite3...")
    result = os.popen("sqlite3 --version").read()
    if result.strip():
        print(f"[✓] sqlite3 versi {result.strip()} tersedia.")
    else:
        print("[✗] sqlite3 tidak ditemukan. Coba install ulang dengan: pkg install sqlite")

def check_python():
    print("[•] Mengecek Python...")
    result = os.popen("python --version").read()
    if result.strip():
        print(f"[✓] Python versi {result.strip()} tersedia.")
    else:
        print("[✗] Python tidak ditemukan. Coba install ulang dengan: pkg install python")

def main():
    print("=== 🔧 Setup & Validasi Termux untuk Inject Roblox Cookie ===\n")
    check_and_install("python")
    check_and_install("sqlite3")
    check_and_install("coreutils")
    check_and_install("busybox")
    check_su_access()
    check_sqlite3()
    check_python()
    print("\n[✓] Semua pengecekan selesai. Siap untuk inject!")

if __name__ == "__main__":
    main()
