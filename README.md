# Zuzulako

A personal session extraction tool that collects Instagram session cookies from browsers on any family machine and uploads them to EDITH (running on Raspberry Pi) for further use.

---

## What It Does

1. Detects the OS (Linux / Windows)
2. Scans all installed browsers (Chrome, Firefox, Brave, Edge, Opera) for an active Instagram session
3. Resolves the Instagram username and user ID from the session
4. Saves session details to `session_store.json`
5. Uploads the JSON file to EDITH's upload API

---

## Files

```
zuzulako/
├── install_run.sh       # For Linux (Arch, Ubuntu, Debian, etc.)
└── install_run.ps1      # For Windows
```

No separate Python file needed — the Python code is embedded inside each script.

---

## Configuration

Before running, set EDITH's IP address at the top of the script:

**Linux (`install_run.sh`):**
```bash
EDITH_UPLOAD_URL="http://<raspberry-pi-ip>:9090/upload"
```

**Windows (`install_run.ps1`):**
```powershell
$EDITH_UPLOAD_URL = "http://<raspberry-pi-ip>:9090/upload"
```

Replace `<raspberry-pi-ip>` with the actual local IP of your Raspberry Pi (e.g. `192.168.1.10`).

---

## Requirements

- Python 3 installed
- pip available
- Instagram must be logged in on at least one browser on the machine
- Network access to EDITH's Raspberry Pi on port `9090`

---

## Usage

### Linux
```bash
chmod +x install_run.sh
./install_run.sh
```

### Windows (Run PowerShell as Administrator)
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\install_run.ps1
```

---

## Output — session_store.json

```json
{
  "dev0root": {
    "username": "dev0root",
    "user_id": "123456789",
    "sessionid": "abc123xyz...",
    "browser": "brave",
    "os": "Linux",
    "machine": "arch-box"
  },
  "moms_username": {
    "username": "moms_username",
    "user_id": "987654321",
    "sessionid": "xyz789abc...",
    "browser": "chrome",
    "os": "Windows",
    "machine": "DESKTOP-MOM"
  }
}
```

Each account gets its own entry keyed by Instagram username. If the username cannot be resolved, the key falls back to `machinename_browsername`.

---

## EDITH Upload API

The script sends a POST request to EDITH on completion:

```
POST http://<edith-ip>:9090/upload
  file        → session_store.json
  message     → "<MACHINE> (<OS>)"
  os_name     → OS name string
```

---

## Notes

- Run this script once per machine per account
- Each run appends to the existing `session_store.json` without overwriting other entries
- Sessions expire if you log out of Instagram on that browser — re-run the script to refresh
- EDITH handles all messaging logic — this tool only handles extraction and upload

---

## Disclaimer

This tool is strictly for personal and family use on accounts you own. Automated session extraction and use of unofficial Instagram APIs may violate Instagram's Terms of Service. Use responsibly.
