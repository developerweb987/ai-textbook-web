@echo off
echo Checking if Chrome remote debugging is available on http://localhost:9222/json...
curl -s http://localhost:9222/json > nul 2>&1
if %errorlevel% == 0 (
    echo SUCCESS: Chrome remote debugging is available!
    echo Here are the available targets:
    curl -s http://localhost:9222/json | python -m json.tool
) else (
    echo ERROR: Could not connect to Chrome remote debugging.
    echo Please make sure Chrome is running with --remote-debugging-port=9222
)
pause