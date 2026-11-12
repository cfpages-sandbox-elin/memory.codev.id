# Deploy memory.codev.id to Cloudflare Pages
param(
    [string]$Profile = "sandbox-elin"
)

$ErrorActionPreference = "Stop"

# 1. Export fresh memory data
$exportScript = Join-Path $PSScriptRoot "export-data.py"
if (Test-Path $exportScript) {
    Write-Host "Exporting fresh memory snapshot..." -ForegroundColor Cyan
    & python.exe "$exportScript"
}

# 2. Map injected AgentSecrets tokens
if ($env:CLOUDFLARE_SANDBOX_ELIN_API_TOKEN) {
    $env:CLOUDFLARE_API_TOKEN = $env:CLOUDFLARE_SANDBOX_ELIN_API_TOKEN
} elseif ($env:CLOUDFLARE_CODEV_MASTER_API_TOKEN) {
    $env:CLOUDFLARE_API_TOKEN = $env:CLOUDFLARE_CODEV_MASTER_API_TOKEN
}

$env:CLOUDFLARE_ACCOUNT_ID = "fc77abc2be8d58e1f81030b2e9a4198b"

$projectRoot = Split-Path $PSScriptRoot -Parent
Write-Host "Deploying $projectRoot to Cloudflare Pages (memory-codev-id)..." -ForegroundColor Cyan

& npx.cmd wrangler pages deploy "$projectRoot" --project-name memory-codev-id --branch main --commit-dirty=true
