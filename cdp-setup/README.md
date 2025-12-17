# Complete MCP/CDP Setup for Chrome Remote Debugging

This setup provides everything you need to work with Chrome DevTools Protocol (CDP) for automation and debugging.

## Prerequisites

1. **Google Chrome** (or Chromium) installed on your system
2. **Node.js** (for Node.js examples) - version 12 or higher
3. **Python** (for Python examples) - version 3.7 or higher
4. **pip** (Python package manager)

## Installation Instructions

### For Python (pyppeteer):
```bash
pip install pyppeteer
```

Or if you have the requirements.txt file:
```bash
pip install -r requirements.txt
```

Note: Pyppeteer will automatically download and manage a bundled version of Chromium, but our setup connects to an existing Chrome instance.

### For Node.js (chrome-remote-interface):
```bash
npm install chrome-remote-interface
```

Or if you have the package.json file:
```bash
npm install
```

## Usage Instructions

### Step 1: Launch Chrome with Remote Debugging

#### On Windows:
- **Using Batch Script:**
  ```cmd
  launch_chrome_debugging.bat
  ```

- **Using PowerShell:**
  ```powershell
  .\launch_chrome_debugging.ps1
  ```

- **Manual Command:**
  ```cmd
  "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"
  ```

#### On macOS:
```bash
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug"
```

#### On Linux:
```bash
google-chrome --remote-debugging-port=9222 --user-data-dir="/tmp/chrome_debug"
```

Or using the shell script:
```bash
chmod +x launch_chrome_debugging.sh
./launch_chrome_debugging.sh
```

### Step 2: Verify the Endpoint

Once Chrome is running with remote debugging, verify the endpoint:

#### On Windows:
- **Using Batch Script:**
  ```cmd
  verify_endpoint.bat
  ```

- **Using PowerShell:**
  ```powershell
  .\verify_endpoint.ps1
  ```

- **Manual Command:**
  ```cmd
  curl http://localhost:9222/json
  ```

#### On macOS/Linux:
```bash
curl http://localhost:9222/json
```

Or using the shell script:
```bash
chmod +x verify_endpoint.sh
./verify_endpoint.sh
```

### Step 3: Run the Python Example

```bash
python chrome_cdp_pyppeteer.py
```

### Step 4: Run the Node.js Example

```bash
node chrome_cdp_node.js
```

## Cross-Platform Compatibility

This setup includes scripts for:
- **Windows**: .bat and .ps1 files
- **macOS/Linux**: .sh files

The Python and Node.js scripts are designed to work across platforms, detecting the OS when needed.

## Troubleshooting

1. **Port Already in Use**: If port 9222 is already in use, change the port number in all scripts and commands.

2. **Permission Issues**: On Unix systems, make sure the shell scripts are executable:
   ```bash
   chmod +x *.sh
   ```

3. **Chrome Not Found**: Update the Chrome path in the scripts if Chrome is installed in a different location.

4. **Connection Refused**: Make sure Chrome is running with remote debugging enabled before running the client scripts.

## Security Considerations

- The remote debugging port (9222) exposes Chrome to potential security risks
- Only use this setup in secure environments
- Close Chrome when not actively using the debugging features
- Consider using the --disable-web-security flag only when necessary for development

## Additional Resources

- [Chrome DevTools Protocol Documentation](https://chromedevtools.github.io/devtools-protocol/)
- [Pyppeteer Documentation](https://pyppeteer.github.io/)
- [Chrome Remote Interface Documentation](https://github.com/cyrus-and/chrome-remote-interface)

## Files Included

- `launch_chrome_debugging.*`: Scripts to launch Chrome with remote debugging
- `verify_endpoint.*`: Scripts to verify the debugging endpoint
- `chrome_cdp_pyppeteer.py`: Python example using pyppeteer
- `chrome_cdp_node.js`: Node.js example using chrome-remote-interface
- `package.json`: Node.js dependencies
- `requirements.txt`: Python dependencies