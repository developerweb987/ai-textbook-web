#!/bin/bash
echo "Launching Chrome with remote debugging on port 9222..."

# Detect OS and launch Chrome accordingly
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Linux
    if command -v google-chrome &> /dev/null; then
        google-chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome_debug &
    elif command -v chromium-browser &> /dev/null; then
        chromium-browser --remote-debugging-port=9222 --user-data-dir=/tmp/chrome_debug &
    else
        echo "Chrome/Chromium not found in PATH"
        exit 1
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    if [ -d "/Applications/Google Chrome.app" ]; then
        /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --remote-debugging-port=9222 --user-data-dir=/tmp/chrome_debug &
    else
        echo "Chrome not found at expected location on macOS"
        exit 1
    fi
else
    echo "Unsupported operating system: $OSTYPE"
    exit 1
fi

echo "Chrome launched with remote debugging. Check http://localhost:9222/json to verify."