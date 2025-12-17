Write-Host "Launching Chrome with remote debugging on port 9222..."
$chromePath = "C:\Program Files\Google\Chrome\Application\chrome.exe"
if (Test-Path $chromePath) {
    Start-Process -FilePath $chromePath -ArgumentList "--remote-debugging-port=9222", "--user-data-dir=C:\temp\chrome_debug"
    Write-Host "Chrome launched with remote debugging. Check http://localhost:9222/json to verify."
} else {
    Write-Host "Chrome not found at expected location. Please install Chrome or update the path."
}
Read-Host -Prompt "Press Enter to exit"