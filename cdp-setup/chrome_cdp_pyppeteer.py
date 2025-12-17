"""
Python script to connect to Chrome with remote debugging using pyppeteer
and evaluate document.title on a webpage.
"""
import asyncio
import pyppeteer
import json
import sys


async def connect_to_existing_chrome():
    """
    Connect to an existing Chrome instance with remote debugging enabled
    """
    try:
        # Connect to the existing Chrome instance
        browser = await pyppeteer.connect(
            browserWSEndpoint='ws://localhost:9222/devtools/browser',
            defaultViewport=None
        )

        print("Connected to existing Chrome instance!")

        # Create a new page
        page = await browser.newPage()

        # Navigate to Google
        print("Navigating to https://www.google.com...")
        await page.goto('https://www.google.com', waitUntil='networkidle2')

        # Evaluate and print the document title
        title = await page.title()
        print(f"Document title: {title}")

        # Alternative way to get title using evaluate
        title_alt = await page.evaluate('document.title')
        print(f"Document title (via evaluate): {title_alt}")

        # Close the page but keep browser connection alive
        await page.close()

        print("Task completed successfully!")

    except Exception as e:
        print(f"Error connecting to Chrome: {str(e)}")
        import traceback
        traceback.print_exc()


async def create_new_chrome_with_debugging():
    """
    Alternative function that creates a new Chrome instance with debugging enabled
    """
    try:
        # Launch Chrome with remote debugging
        browser = await pyppeteer.launch(
            headless=False,
            args=['--remote-debugging-port=9222']
        )

        print("Launched new Chrome instance with remote debugging!")

        # Create a new page
        page = await browser.newPage()

        # Navigate to Google
        print("Navigating to https://www.google.com...")
        await page.goto('https://www.google.com', waitUntil='networkidle2')

        # Evaluate and print the document title
        title = await page.title()
        print(f"Document title: {title}")

        # Alternative way to get title using evaluate
        title_alt = await page.evaluate('document.title')
        print(f"Document title (via evaluate): {title_alt}")

        print("Keep this script running to maintain the Chrome instance...")
        print("Press Ctrl+C to exit and close Chrome.")

        # Keep the script running
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\nClosing Chrome...")
            await browser.close()

    except Exception as e:
        print(f"Error launching Chrome: {str(e)}")
        import traceback
        traceback.print_exc()


def check_debugging_targets():
    """
    Check what targets are available via the debugging protocol
    """
    import urllib.request
    import json

    try:
        response = urllib.request.urlopen('http://localhost:9222/json')
        data = response.read()
        targets = json.loads(data)

        print("Available debugging targets:")
        for target in targets:
            print(f"- {target['type']}: {target['url']} (ID: {target['id']})")

        return targets
    except Exception as e:
        print(f"Could not fetch debugging targets: {str(e)}")
        return []


async def main():
    """
    Main function to demonstrate both connection methods
    """
    print("Chrome DevTools Protocol (CDP) Python Example")
    print("="*50)

    # Check what targets are available
    check_debugging_targets()

    print("\nChoose an option:")
    print("1. Connect to existing Chrome instance (port 9222)")
    print("2. Launch new Chrome instance with debugging")

    choice = input("Enter choice (1 or 2, default 1): ").strip() or "1"

    if choice == "1":
        await connect_to_existing_chrome()
    elif choice == "2":
        await create_new_chrome_with_debugging()
    else:
        print("Invalid choice, defaulting to option 1")
        await connect_to_existing_chrome()


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())