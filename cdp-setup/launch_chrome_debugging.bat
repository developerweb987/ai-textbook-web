@echo off
echo Launching Chrome with remote debugging on port 9222...
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222 --user-data-dir="C:\temp\chrome_debug"
echo Chrome launched with remote debugging. Check http://localhost:9222/json to verify.
pause