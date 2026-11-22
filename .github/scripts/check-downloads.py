#!/usr/bin/env python3
"""Checks that the wallet downloads bwalletx.com serves are the files download/latest.json describes.

latest.json is what the Android direct updater and the extension's "newer bWalletX" banner trust, so a download that
doesn't match it (wrong file copied, half-finished release, or a swapped file) must never go unnoticed. For every file
latest.json points at under https://bwalletx.com/download/, this compares the committed file's SHA-256 and size, and
checks that the download pages quote the same SHA-256. Exit 1 with a plain list of problems; exit 0 when all match.
"""
import hashlib
import json
import os
import re
import sys

PREFIX = 'https://bwalletx.com/download/'


def entries(doc):
    """(label, url, sha256, size) for the top-level APK and every channel that names a file."""
    yield 'android-direct', doc.get('apk'), doc.get('sha256'), doc.get('size')
    for name, ch in (doc.get('channels') or {}).items():
        if ch.get('url'):
            yield name, ch.get('url'), ch.get('sha256'), ch.get('size')


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1 << 20), b''):
            h.update(block)
    return h.hexdigest()


def main():
    doc = json.load(open('download/latest.json'))
    pages = {p: open(p, encoding='utf-8', errors='replace').read() for p in os.listdir('.') if p.endswith('.html')}
    problems = []
    checked = 0
    for label, url, want_sha, want_size in entries(doc):
        if not url or not url.startswith(PREFIX):
            problems.append(f'{label}: url {url!r} is not under {PREFIX}')
            continue
        path = 'download/' + url[len(PREFIX):]
        if not re.fullmatch(r'download/[A-Za-z0-9._-]+', path) or not os.path.isfile(path):
            problems.append(f'{label}: {path} is missing from the repo')
            continue
        got_sha, got_size = sha256(path), os.path.getsize(path)
        checked += 1
        if got_sha != (want_sha or '').lower():
            problems.append(f'{label}: {path} SHA-256 is {got_sha}, latest.json says {want_sha}')
        if want_size is not None and got_size != want_size:
            problems.append(f'{label}: {path} is {got_size} bytes, latest.json says {want_size}')
        quoting = [p for p, text in pages.items() if os.path.basename(path) in text and re.search(r'\b[0-9a-f]{64}\b', text)]
        for p in quoting:
            if got_sha not in pages[p]:
                problems.append(f'{label}: {p} links {os.path.basename(path)} but does not quote its SHA-256 {got_sha}')
    if not checked:
        problems.append('latest.json names no downloadable file')
    for line in problems:
        print('PROBLEM ' + line)
    print(f'{checked} download(s) checked, {len(problems)} problem(s)')
    return 1 if problems else 0


if __name__ == '__main__':
    sys.exit(main())
