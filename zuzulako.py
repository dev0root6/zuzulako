import browser_cookie3
import requests
import json
import os
import platform
import socket

SESSION_FILE = "session_store.json"

# --- STEP 1: Detect OS and try all supported browsers ---
def get_session_id():
    system = platform.system()  # Linux / Windows / Darwin

    # Map browser names to browser_cookie3 functions
    browsers = {
        "chrome": browser_cookie3.chrome,
        "firefox": browser_cookie3.firefox,
        "brave": browser_cookie3.brave,
        "edge": browser_cookie3.edge,
        "opera": browser_cookie3.opera,
    }

    # Safari only on macOS
    if system == "Darwin":
        browsers["safari"] = browser_cookie3.safari

    found = []

    for browser_name, browser_fn in browsers.items():
        try:
            cookies = browser_fn(domain_name=".instagram.com")
            for c in cookies:
                if c.name == "sessionid":
                    print(f"[+] Found sessionid in {browser_name} ({system})")
                    found.append({
                        "browser": browser_name,
                        "sessionid": c.value
                    })
                    break
        except Exception:
            pass

    if not found:
        print("[-] No Instagram session found in any browser.")
        exit(1)

    # If multiple browsers found, pick first (or could prompt user)
    if len(found) > 1:
        print(f"[!] Multiple sessions found: {[f['browser'] for f in found]}")
        print(f"[~] Using: {found[0]['browser']}")

    return found[0]["sessionid"], found[0]["browser"], system

# --- STEP 2: Identify Instagram username from session ---
def get_username(session_id):
    try:
        headers = {
            "cookie": f"sessionid={session_id}",
            "x-ig-app-id": "936619743392459",
            "user-agent": "Mozilla/5.0"
        }
        r = requests.get(
            "https://www.instagram.com/api/v1/accounts/current_user/?edit=true",
            headers=headers,
            timeout=10
        )
        data = r.json()
        username = data["user"]["username"]
        user_id = data["user"]["pk"]
        return username, str(user_id)
    except Exception:
        return None, None

# --- STEP 3: Save to session_store.json ---
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

    print(f"[✓] Session saved → key: '{key}' | machine: {machine} | browser: {browser} | os: {system}")

# --- MAIN ---
if __name__ == "__main__":
    session_id, browser, system = get_session_id()
    username, user_id = get_username(session_id)

    if username:
        print(f"[+] Instagram account: @{username} (ID: {user_id})")
    else:
        print("[!] Could not resolve Instagram username — saving with machine/browser info only.")

    save_session(session_id, browser, system, username, user_id)
