$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$projectEnvPath = Join-Path $projectRoot '.env'
$projectConfPath = Join-Path $projectRoot 'config/odoo.conf'
$envExists = Test-Path -LiteralPath $projectEnvPath
$confExists = Test-Path -LiteralPath $projectConfPath

if ($envExists -and $confExists) {
    Write-Output 'Konfigurasi sudah ada. Tidak ada file yang diganti.'
    exit 0
}
if ($envExists -or $confExists) {
    throw 'Konfigurasi baru tersedia sebagian. Periksa .env dan config/odoo.conf. Tidak ada file yang diganti.'
}

function New-LocalHexSecret {
    $randomBytes = New-Object byte[] 24
    $generator = [System.Security.Cryptography.RandomNumberGenerator]::Create()
    try {
        $generator.GetBytes($randomBytes)
    }
    finally {
        $generator.Dispose()
    }
    return ([System.BitConverter]::ToString($randomBytes)).Replace('-', '').ToLowerInvariant()
}

$envTemplatePath = Join-Path $projectRoot '.env.example'
$confTemplatePath = Join-Path $projectRoot 'config/odoo.conf.example'
$envText = [System.IO.File]::ReadAllText($envTemplatePath)
$confText = [System.IO.File]::ReadAllText($confTemplatePath)
if (-not $envText.Contains('CHANGE_ME_DATABASE_PASSWORD')) {
    throw 'Template .env tidak memiliki penanda password yang diperlukan.'
}
if (-not $confText.Contains('CHANGE_ME_MASTER_PASSWORD')) {
    throw 'Template Odoo tidak memiliki penanda master password yang diperlukan.'
}
$pgSecret = New-LocalHexSecret
$masterSecret = New-LocalHexSecret
$envText = $envText.Replace('CHANGE_ME_DATABASE_PASSWORD', $pgSecret)
$confText = $confText.Replace('CHANGE_ME_MASTER_PASSWORD', $masterSecret)
$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText($projectEnvPath, $envText, $utf8)
[System.IO.File]::WriteAllText($projectConfPath, $confText, $utf8)
Write-Output 'Siap. .env dan config/odoo.conf dibuat dengan password lokal baru.'
Write-Output 'Master password untuk membuat database ada pada admin_passwd di config/odoo.conf.'
Write-Output 'Berikutnya jalankan: docker compose up -d'
