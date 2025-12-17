#!/usr/bin/env python3
"""
Cross-platform Chrome CDP launcher and tester
This script handles launching Chrome with remote debugging and running tests across platforms
"""
import os
import sys
import subprocess
import platform
import time
import json
import urllib.request
from pathlib import Path


def get_chrome_path():
    """Get the Chrome executable path based on the operating system"""
    system = platform.system()

    if system == "Windows":
        # Check common Windows Chrome installation paths
        possible_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            r"C:\Users\%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"
        ]

        for path in possible_paths:
            expanded_path = os.path.expandvars(path)
            if os.path.exists(expanded_path):
                return expanded_path
    elif system == "Darwin":  # macOS
        mac_paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary"
        ]

        for path in mac_paths:
            if os.path.exists(path):
                return path
    else:  # Linux and others
        # Check if chrome/chromium is in PATH
        for cmd in ['google-chrome', 'chromium-browser', 'chromium', 'google-chrome-stable']:
            if subprocess.call(['which', cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0:
                return cmd

        # Check common Linux installation paths
        linux_paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium"
        ]

        for path in linux_paths:
            if os.path.exists(path):
                return path

    return None


def launch_chrome_with_debugging(port=9222):
    """Launch Chrome with remote debugging enabled"""
    chrome_path = get_chrome_path()

    if not chrome_path:
        print("❌ Chrome not found on this system!")
        print("Please install Chrome or Chromium and try again.")
        return False

    print(f"✅ Found Chrome at: {chrome_path}")

    # Choose user data directory based on OS
    if platform.system() == "Windows":
        user_data_dir = os.path.join(os.environ.get("TEMP", "C:\\temp"), "chrome_debug")
    else:
        user_data_dir = os.path.join(os.path.sep, "tmp", "chrome_debug")

    # Ensure the user data directory exists
    os.makedirs(user_data_dir, exist_ok=True)

    print(f"🚀 Launching Chrome with remote debugging on port {port}...")

    try:
        if platform.system() == "Windows":
            # On Windows, use subprocess.Popen to launch Chrome in the background
            subprocess.Popen([
                chrome_path,
                f"--remote-debugging-port={port}",
                f"--user-data-dir={user_data_dir}",
                "--no-first-run",
                "--no-default-browser-check"
            ])
        else:
            # On Unix-like systems, use subprocess.Popen with appropriate flags
            subprocess.Popen([
                chrome_path,
                f"--remote-debugging-port={port}",
                f"--user-data-dir={user_data_dir}",
                "--no-first-run",
                "--no-default-browser-check"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, start_new_session=True)

        print(f"✅ Chrome launched with remote debugging on port {port}")
        print(f"📁 User data directory: {user_data_dir}")
        return True
    except Exception as e:
        print(f"❌ Error launching Chrome: {str(e)}")
        return False


def verify_debugging_endpoint(port=9222):
    """Verify that the Chrome debugging endpoint is accessible"""
    try:
        url = f"http://localhost:{port}/json"
        response = urllib.request.urlopen(url, timeout=5)
        data = response.read()
        targets = json.loads(data.decode('utf-8'))

        print(f"✅ Successfully connected to Chrome debugging endpoint!")
        print(f"📊 Found {len(targets)} debugging target(s):")

        for i, target in enumerate(targets):
            print(f"   {i+1}. {target.get('type', 'unknown')}: {target.get('url', 'no-url')} (ID: {target.get('id', 'no-id')[:8]}...)")

        return True
    except Exception as e:
        print(f"❌ Could not connect to Chrome debugging endpoint: {str(e)}")
        print("💡 Make sure Chrome is running with --remote-debugging-port flag")
        return False


def test_python_cdp_connection():
    """Test CDP connection using Python/pyppeteer"""
    try:
        import pyppeteer
        print("✅ Pyppeteer is available")
        return True
    except ImportError:
        print("❌ Pyppeteer not found. Install with: pip install pyppeteer")
        return False


def test_node_cdp_connection():
    """Test if Node.js and chrome-remote-interface are available"""
    try:
        # Check if node is available
        result = subprocess.run(['node', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("❌ Node.js not found. Please install Node.js")
            return False

        print(f"✅ Node.js version: {result.stdout.strip()}")

        # Check if chrome-remote-interface is installed in the local directory
        node_modules_path = Path(__file__).parent / "node_modules" / "chrome-remote-interface"
        if not node_modules_path.exists():
            print("⚠️  chrome-remote-interface not found in node_modules")
            print("💡 Install with: npm install chrome-remote-interface")
        else:
            print("✅ chrome-remote-interface is available")

        return True
    except subprocess.TimeoutExpired:
        print("❌ Timeout checking Node.js")
        return False
    except FileNotFoundError:
        print("❌ Node.js not found. Please install Node.js")
        return False
    except Exception as e:
        print(f"❌ Error checking Node.js: {str(e)}")
        return False


def main():
    """Main function to run the complete setup test"""
    print("🔍 Chrome DevTools Protocol (CDP) Cross-Platform Setup")
    print("=" * 60)
    print(f"Operating System: {platform.system()} {platform.release()}")
    print(f"Python Version: {sys.version}")
    print()

    # Step 1: Check prerequisites
    print("📋 Checking prerequisites...")
    python_available = test_python_cdp_connection()
    node_available = test_node_cdp_connection()
    print()

    # Step 2: Launch Chrome with debugging
    print("🌐 Launching Chrome with remote debugging...")
    chrome_launched = launch_chrome_with_debugging(9222)
    print()

    if chrome_launched:
        # Give Chrome a moment to start
        print("⏳ Waiting for Chrome to initialize...")
        time.sleep(3)

        # Step 3: Verify the endpoint
        print("📡 Verifying debugging endpoint...")
        endpoint_accessible = verify_debugging_endpoint(9222)
        print()

        if endpoint_accessible:
            print("🎉 Chrome CDP setup is working correctly!")
            print()
            print("🚀 Next steps:")
            print("   1. Run Python example: python chrome_cdp_pyppeteer.py")
            print("   2. Run Node.js example: node chrome_cdp_node.js")
            print()
            print("💡 Tip: Keep Chrome running while using the CDP clients")
        else:
            print("❌ Chrome debugging endpoint is not accessible")
            print("💡 Make sure Chrome is running with --remote-debugging-port=9222")
    else:
        print("❌ Could not launch Chrome with remote debugging")
        print("💡 Make sure Chrome is properly installed on your system")

    print()
    print("📖 For detailed instructions, see README.md")


if __name__ == "__main__":
    main()