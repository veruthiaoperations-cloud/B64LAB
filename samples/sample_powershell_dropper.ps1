# ==============================================================================
# B64Lab Forensic Sample: PowerShell Dropper Script (Defanged Educational Sample)
# MITRE ATT&CK: T1059.001 (PowerShell), T1027 (Obfuscated Files or Information)
# ==============================================================================

<#
  Incident Scenario:
  This script was identified executing in an enterprise environment under a
  scheduled task. Notice how the command uses -EncodedCommand to pass a UTF-16LE
  Base64 string to bypass basic string inspection.
#>

$TargetScript = "VwByAGkAdABlAC0ASABvAHMAdAAgACcAWwBCAAAANgA0AEwAYQBiAF0AIABTAGEAbQBwAGwAZQAgAFMAYwByAGkAcAB0ACAARQB4AGUAYwB1AHQAZQBkACEAJwAgAC0ARgBvAHIAZQBnAHIAbwB1AG4AZABDAG8AbABvAHIAIABDAHkAYQBuAA=="

Write-Host "[*] Staging execution..." -ForegroundColor Yellow
# powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -EncodedCommand $TargetScript
