import os, time

# Daftar paket yang tersedia
pkgs = [
    "com.mangcut.rulod",
    "com.mangcut.ruloe",
    "com.mangcut.rulof",
    "com.mangcut.rulog",
    # Tambahkan hingga 8 jika perlu
]

# Minta jumlah yang akan dijalankan
jumlah = int(input(f"Berapa pkg yang ingin dijalankan? (1-{len(pkgs)}): "))
selected_pkgs = pkgs[:jumlah]

# Loop untuk setiap pkg yang dipilih
for i, pkg in enumerate(selected_pkgs, start=1):
    print(f"\n[•] {pkg} meminta cookie akun ke {i}")
    cookie = input("Masukkan cookie: ").strip()

    db_path = f"/data/data/{pkg}/app_webview/Default/Cookies"
    sql_path = "/sdcard/Download/inject.sql"

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
    with open(sql_path, "w") as f:
        f.write(sql)

    print(f"[+] Inject cookie ke {pkg}...")
    os.system(f"sqlite3 {db_path} < {sql_path}")
    os.system(f"su -c 'chmod 444 {db_path}'")

    print(f"[+] Menutup {pkg} dulu...")
    os.system(f"su -c 'am force-stop {pkg}'")
    time.sleep(1)

    print(f"[+] Membuka {pkg}...")
    os.system(f"su -c 'monkey -p {pkg} -c android.intent.category.LAUNCHER 1'")
    time.sleep(4)

print(f"\n[✓] Selesai inject dan buka semua app")
