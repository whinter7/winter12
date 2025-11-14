#!/usr/bin/env python
""":"
PY=$(command -v python3 || command -v python)
exec $PY "$0" "$@"
":"""

import os
import shutil

def cek(pkg):
    print("[•] cek", pkg)
    if shutil.which(pkg) is None:
        print("[!] install", pkg)
        os.system("pkg install -y " + pkg)
    else:
        print("[✓] ok:", pkg)

def main():
    cek("python")
    cek("sqlite3")
    cek("coreutils")
    cek("busybox")
    print("[•] cek root")
    out = os.popen("su -c id").read()
    if "uid=0" in out:
        print("[✓] root ok")
    else:
        print("[✗] tidak root")

if __name__ == "__main__":
    main()
