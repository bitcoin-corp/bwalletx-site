#!/usr/bin/env python3
"""Write download/latest.json for the Android direct APK's in-app updater (bWalletX Settings › About).

  python3 scripts/latest-json.py <version> <versionCode> [path/to/SHA256SUMS-direct]

The SHA-256 comes from SHA256SUMS-direct (the line for bwallet-<version>-direct.apk) when given, and must
equal the hash of download/bwalletx-android-<version>.apk here; size is that file's size.
"""
import hashlib, json, os, re, sys

if len(sys.argv) not in (3, 4):
    sys.exit(__doc__)
ver, code = sys.argv[1], int(sys.argv[2])
if not re.fullmatch(r"\d+(\.\d+)*", ver) or code <= 0:
    sys.exit("bad version / versionCode")
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
apk = os.path.join(root, "download", f"bwalletx-android-{ver}.apk")
h = hashlib.sha256()
with open(apk, "rb") as f:
    for chunk in iter(lambda: f.read(1 << 20), b""):
        h.update(chunk)
sha = h.hexdigest()
if len(sys.argv) == 4:
    want = None
    for line in open(sys.argv[3]):
        parts = line.split()
        if len(parts) == 2 and parts[1].lstrip("*") == f"bwallet-{ver}-direct.apk":
            want = parts[0].lower()
    if want is None:
        sys.exit(f"bwallet-{ver}-direct.apk not in {sys.argv[3]}")
    if want != sha:
        sys.exit(f"SHA-256 mismatch: SHA256SUMS-direct {want} vs {apk} {sha}")
out = {
    "version": ver,
    "versionCode": code,
    "apk": f"https://bwalletx.com/download/bwalletx-android-{ver}.apk",
    "sha256": sha,
    "size": os.path.getsize(apk),
    "notes_url": f"https://bwalletx.com/releases#v{ver}",
}
with open(os.path.join(root, "download", "latest.json"), "w") as f:
    json.dump(out, f, indent=2)
    f.write("\n")
print(json.dumps(out, indent=2))
