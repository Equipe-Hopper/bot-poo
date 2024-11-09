$exclude = @("venv", "Bot_poo.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "Bot_poo.zip" -Force