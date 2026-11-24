# Revisión de la computadora del estudio para el proyecto 3D de Pipo y Plop.
# Uso (PowerShell, no hace falta ser administrador):
#   powershell -ExecutionPolicy Bypass -File 3d\herramientas\revisar_pc.ps1
# Solo lee información del sistema: no instala ni cambia nada.
# Guarda el informe en revision_pc.txt, en la carpeta desde donde se ejecuta.

$out = @()
function Linea($t) { $script:out += $t; Write-Host $t }
function OK($c, $t) { if ($c) { Linea "  [OK]  $t" } else { Linea "  [!!]  $t" } }

Linea "Revisión de la PC · $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Linea "=================================================="

# Sistema
$os = Get-CimInstance Win32_OperatingSystem
Linea "`nSistema: $($os.Caption) $($os.Version) ($($os.OSArchitecture))"

# Procesador
$cpu = Get-CimInstance Win32_Processor | Select-Object -First 1
Linea "`nProcesador: $($cpu.Name.Trim())"
Linea "  Núcleos: $($cpu.NumberOfCores) · hilos: $($cpu.NumberOfLogicalProcessors)"
OK ($cpu.NumberOfCores -ge 16) "Núcleos suficientes para render y simulación"

# Memoria
$mods = Get-CimInstance Win32_PhysicalMemory
$gb = [math]::Round(($mods | Measure-Object Capacity -Sum).Sum / 1GB)
Linea "`nMemoria RAM: $gb GB en $($mods.Count) módulo(s)"
foreach ($m in $mods) { Linea "  - $([math]::Round($m.Capacity/1GB)) GB · $($m.Speed) MT/s (configurada $($m.ConfiguredClockSpeed)) · $($m.Manufacturer) $($m.PartNumber.Trim())" }
OK ($gb -ge 32) "32 GB o más (recomendado para Blender + DaVinci)"
$vel = ($mods | Select-Object -First 1).ConfiguredClockSpeed
$max = ($mods | Select-Object -First 1).Speed
OK ($vel -ge $max -or $vel -ge 5200) "La memoria corre a su velocidad (si no, activar XMP/EXPO en la BIOS)"

# Tarjeta gráfica
Linea "`nTarjeta gráfica:"
$smi = "$env:ProgramFiles\NVIDIA Corporation\NVSMI\nvidia-smi.exe"
if (-not (Test-Path $smi)) { $smi = (Get-Command nvidia-smi -ErrorAction SilentlyContinue).Source }
if ($smi) {
  $g = & $smi --query-gpu=name,driver_version,memory.total,pcie.link.gen.current,pcie.link.width.current --format=csv,noheader
  Linea "  $g"
  $drv = [double](($g -split ',')[1].Trim())
  OK ($drv -ge 570) "Driver NVIDIA reciente (la serie RTX 50 necesita drivers 570 o posteriores)"
} else {
  Get-CimInstance Win32_VideoController | ForEach-Object { Linea "  $($_.Name) · driver $($_.DriverVersion)" }
  Linea "  [!!]  No se encontró nvidia-smi: instala o actualiza el driver NVIDIA (Studio Driver recomendado)"
}

# Discos
Linea "`nDiscos:"
Get-CimInstance Win32_LogicalDisk -Filter "DriveType=3" | ForEach-Object {
  $libre = [math]::Round($_.FreeSpace/1GB); $total = [math]::Round($_.Size/1GB)
  Linea "  $($_.DeviceID) $libre GB libres de $total GB"
}
$c = Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
OK ([math]::Round($c.FreeSpace/1GB) -ge 300) "Al menos 300 GB libres en C: para proyectos, cachés y renders"
Get-PhysicalDisk | ForEach-Object { Linea "  Disco físico: $($_.FriendlyName) · $($_.MediaType) · $([math]::Round($_.Size/1GB)) GB · salud $($_.HealthStatus)" }

# Energía
$plan = (powercfg /getactivescheme) -join ' '
Linea "`nPlan de energía: $plan"
OK ($plan -match 'Alto rendimiento|High performance|Máximo|Ultimate|Equilibrado|Balanced') "Plan de energía activo"

# Programas del proyecto
Linea "`nProgramas:"
function Prog($nombre, $cmd, $rutas) {
  $p = Get-Command $cmd -ErrorAction SilentlyContinue
  if (-not $p) { foreach ($r in $rutas) { $hit = Get-ChildItem $r -ErrorAction SilentlyContinue | Select-Object -First 1; if ($hit) { $p = $hit; break } } }
  if ($p) { $ruta = if ($p.Source) { $p.Source } else { $p.FullName }; Linea "  [OK]  $nombre · $ruta" } else { Linea "  [--]  $nombre no instalado" }
}
Prog "Blender" "blender" @("$env:ProgramFiles\Blender Foundation\Blender*\blender.exe")
Prog "Git" "git" @("$env:ProgramFiles\Git\cmd\git.exe")
Prog "Python" "python" @("$env:LocalAppData\Programs\Python\Python3*\python.exe")
Prog "Node.js" "node" @("$env:ProgramFiles\nodejs\node.exe")
Prog "FFmpeg" "ffmpeg" @()
Prog "DaVinci Resolve" "Resolve" @("$env:ProgramFiles\Blackmagic Design\DaVinci Resolve\Resolve.exe")
Prog "Claude (app de escritorio)" "claude" @("$env:LocalAppData\AnthropicClaude\claude.exe", "$env:LocalAppData\Programs\claude\Claude.exe")

$b = Get-Command blender -ErrorAction SilentlyContinue
if (-not $b) { $b = Get-ChildItem "$env:ProgramFiles\Blender Foundation\Blender*\blender.exe" -ErrorAction SilentlyContinue | Select-Object -First 1 }
if ($b) {
  $bp = if ($b.Source) { $b.Source } else { $b.FullName }
  $ver = & $bp --version 2>$null | Select-Object -First 1
  Linea "  Blender: $ver"
}

# Monitor
Linea "`nMonitores:"
Get-CimInstance -Namespace root\wmi -ClassName WmiMonitorID -ErrorAction SilentlyContinue | ForEach-Object {
  $n = ($_.UserFriendlyName | Where-Object { $_ -ne 0 } | ForEach-Object { [char]$_ }) -join ''
  Linea "  $n"
}
Get-CimInstance Win32_VideoController | ForEach-Object { Linea "  Modo actual: $($_.CurrentHorizontalResolution)x$($_.CurrentVerticalResolution) a $($_.CurrentRefreshRate) Hz" }

$out | Out-File -Encoding utf8 revision_pc.txt
Linea "`nInforme guardado en $(Resolve-Path revision_pc.txt)"
