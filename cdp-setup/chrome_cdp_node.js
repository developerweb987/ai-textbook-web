/**
 * Node.js script to connect to Chrome with remote debugging using chrome-remote-interface
 * and evaluate document.title on a webpage.
 */

const CDP = require('chrome-remote-interface');
const readline = require('readline');

// Function to list available targets
async function listTargets() {
    try {
        const tabs = await CDP.List();
        console.log('Available debugging targets:');
        tabs.forEach((target, index) => {
            console.log(`${index + 1}. ${target.type}: ${target.url} (ID: ${target.id})`);
        });
        return tabs;
    } catch (err) {
        console.error(`Error listing targets: ${err.message}`);
        return [];
    }
}

// Function to connect to existing Chrome and evaluate document.title
async function connectToExistingChrome() {
    try {
        console.log('Connecting to existing Chrome instance...');

        // List available targets first
        const targets = await listTargets();

        // Connect to Chrome (will connect to the first available browser target)
        const client = await CDP({
            // Connect to the browser endpoint
            host: 'localhost',
            port: 9222
        });

        console.log('Connected to Chrome CDP!');

        const { Runtime, Page, Target } = client;

        // Enable the domains we'll use
        await Page.enable();
        await Runtime.enable();

        // Create a new tab
        const targetId = await Target.createTarget({ url: 'about:blank' });
        const tabClient = await CDP({ target: targetId.targetId });
        const { Page:TabPage, Runtime:TabRuntime } = tabClient;

        await TabPage.enable();
        await TabRuntime.enable();

        // Navigate to Google
        console.log('Navigating to https://www.google.com...');
        await TabPage.navigate({ url: 'https://www.google.com' });
        await TabPage.loadEventFired();

        // Evaluate and print the document title using Runtime
        const result = await TabRuntime.evaluate({ expression: 'document.title' });
        console.log(`Document title: ${result.result.value}`);

        // Clean up
        await tabClient.close();
        await client.close();

        console.log('Task completed successfully!');
    } catch (err) {
        console.error(`Error connecting to Chrome: ${err.message}`);
        console.error(err.stack);
    }
}

// Function to launch Chrome with debugging and connect
async function launchChromeWithDebugging() {
    const spawn = require('child_process').spawn;

    let chromePath;

    // Determine Chrome path based on OS
    switch (process.platform) {
        case 'win32':
            chromePath = [
                'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
                'C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe'
            ].find(require('fs').existsSync);
            break;
        case 'darwin': // macOS
            chromePath = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
            break;
        case 'linux':
            chromePath = 'google-chrome' || 'chromium-browser';
            break;
        default:
            console.error(`Unsupported platform: ${process.platform}`);
            return;
    }

    if (!chromePath) {
        console.error('Chrome not found on this system');
        return;
    }

    console.log(`Launching Chrome with debugging... (path: ${chromePath})`);

    // Launch Chrome with remote debugging
    const chromeProcess = spawn(chromePath, [
        '--remote-debugging-port=9222',
        '--no-first-run',
        '--no-default-browser-check',
        'about:blank'
    ]);

    chromeProcess.stdout.on('data', (data) => {
        console.log(`Chrome stdout: ${data}`);
    });

    chromeProcess.stderr.on('data', (data) => {
        console.error(`Chrome stderr: ${data}`);
    });

    chromeProcess.on('close', (code) => {
        console.log(`Chrome process exited with code ${code}`);
    });

    console.log('Chrome launched with remote debugging. Waiting for endpoint to be available...');

    // Wait a bit for Chrome to start
    setTimeout(async () => {
        try {
            // Connect to the newly launched Chrome
            await connectToExistingChrome();

            console.log('\nKeep this script running to maintain the Chrome instance...');
            console.log('Press Ctrl+C to exit and close Chrome.');

            // Keep the script running
            const rl = readline.createInterface({
                input: process.stdin,
                output: process.stdout
            });

            rl.question('Press Enter to exit...', () => {
                rl.close();
                chromeProcess.kill();
                process.exit(0);
            });

        } catch (err) {
            console.error(`Error: ${err.message}`);
            chromeProcess.kill();
        }
    }, 3000); // Wait 3 seconds for Chrome to start
}

// Main function
async function main() {
    console.log('Chrome DevTools Protocol (CDP) Node.js Example');
    console.log('='*50);

    console.log('\nChoose an option:');
    console.log('1. Connect to existing Chrome instance (port 9222)');
    console.log('2. Launch new Chrome instance with debugging');

    const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
    });

    rl.question('Enter choice (1 or 2, default 1): ', async (choice) => {
        const opt = choice.trim() || '1';

        if (opt === '1') {
            await connectToExistingChrome();
        } else if (opt === '2') {
            await launchChromeWithDebugging();
        } else {
            console.log('Invalid choice, defaulting to option 1');
            await connectToExistingChrome();
        }

        rl.close();
    });
}

// Run the main function
main().catch(console.error);