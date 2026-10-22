$ErrorActionPreference = "Stop"

cd $PSScriptRoot

$project_python = $env:PECUNIA_PYTHON

if ([string]::IsNullOrEmpty($project_python)) {
    if (Get-Command "python3.12" -ErrorAction SilentlyContinue) {
        $project_python = (Get-Command "python3.12").Source
    }
    elseif (Get-Command "python" -ErrorAction SilentlyContinue) {
        $python_test = & python -c "import sys; print(sys.version_info >= (3,12))" 2>$null
        if ($python_test -eq "True") {
            $project_python = (Get-Command "python").Source
        }
    }
    
    if ([string]::IsNullOrEmpty($project_python)) {
        $codex_path = "$env:USERPROFILE\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\Scripts\python.exe"
        if (Test-Path $codex_path) {
            $project_python = $codex_path
        }
    }
    
    if ([string]::IsNullOrEmpty($project_python)) {
        Write-Error "Instale Python 3.12 ou superior e execute novamente."
        exit 1
    }
}

& $project_python -c 'import sys; assert sys.version_info >= (3,12), "Python 3.12+ necessário"'
if ($LASTEXITCODE -ne 0) { exit 1 }

node -e "const [major,minor]=process.versions.node.split('.').map(Number);if(major<20||(major===20&&minor<9))throw new Error('Node.js 20.9+ necessario')"
if ($LASTEXITCODE -ne 0) { exit 1 }

if (Get-Command "uv" -ErrorAction SilentlyContinue) {
    $project_uv = (Get-Command "uv").Source
}
elseif (Test-Path "backend\.venv\Scripts\uv.exe") {
    $project_uv = "$PSScriptRoot\backend\.venv\Scripts\uv.exe"
}
else {
    Write-Host "Instalando o 'uv' em um ambiente temporário..."
    & $project_python -m venv .tooling
    & .tooling\Scripts\python.exe -m pip install 'uv==0.13.4'
    $project_uv = "$PSScriptRoot\.tooling\Scripts\uv.exe"
}

& $project_uv sync --locked --project backend --python "$project_python"

cd frontend
& npm ci --no-audit --no-fund
& npm run contracts:check

$env:NEXT_TELEMETRY_DISABLED = "1"
& npm run build
Remove-Item Env:\NEXT_TELEMETRY_DISABLED  # Limpa a variável após o uso

cd $PSScriptRoot

Write-Host "Ambiente preparado. Execute .\START.ps1 (ou o script equivalente de inicialização do Windows) para operar offline."
