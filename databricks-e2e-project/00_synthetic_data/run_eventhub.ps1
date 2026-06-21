$PSScriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Definition
$python = Join-Path $PSScriptRoot '.venv\Scripts\python.exe'
$script = Join-Path $PSScriptRoot '04_eventhub_orders.py'
& $python $script
