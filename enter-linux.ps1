$ErrorActionPreference = 'Stop'
$wslPath = 'C:\Program Files\WSL\wsl.exe'
if (-not (Test-Path -LiteralPath $wslPath)) { $wslPath = 'C:\Windows\System32\wsl.exe' }
& $wslPath -d SMEFTsim -u smeft --cd /home/smeft/detector-learning
if ($LASTEXITCODE -ne 0) { throw 'Cannot enter the detector-learning Linux project.' }
