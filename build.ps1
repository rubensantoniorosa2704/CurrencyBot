$exclude = @("venv", "CurrencyBot.zip")
$files = Get-ChildItem -Path . -Exclude $exclude
Compress-Archive -Path $files -DestinationPath "CurrencyBot.zip" -Force