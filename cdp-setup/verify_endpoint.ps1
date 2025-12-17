Write-Host "Checking if Chrome remote debugging is available on http://localhost:9222/json..."

try {
    $response = Invoke-RestMethod -Uri "http://localhost:9222/json" -Method Get
    Write-Host "SUCCESS: Chrome remote debugging is available!"
    Write-Host "Here are the available targets:"
    $response | ConvertTo-Json -Depth 5
} catch {
    Write-Host "ERROR: Could not connect to Chrome remote debugging."
    Write-Host "Please make sure Chrome is running with --remote-debugging-port=9222"
}

Read-Host -Prompt "Press Enter to exit"