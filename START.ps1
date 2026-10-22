cd $PSScriptRoot

if (-not (Test-Path "backend\.venv\Scripts\python.exe")) {
    Write-Host "Execute .\setup.ps1 para preparar o ambiente primeiro."
    Read-Host "Pressione Enter para fechar."
    exit 1
}

& backend\.venv\Scripts\python.exe run_local.py

$launcher_status = $LASTEXITCODE

if ($launcher_status -ne 0) {
    Write-Host ""
    Write-Host "O aplicativo não foi iniciado. Confira as instruções acima." -ForegroundColor Red
    Read-Host "Pressione Enter para fechar esta janela."
}

exit $launcher_status
