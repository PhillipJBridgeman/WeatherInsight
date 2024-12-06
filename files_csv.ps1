# Get the current directory where the script is run
$CurrentFolderPath = Get-Location

# Define the output file path (relative to the current folder)
$OutputCSV = Join-Path -Path $CurrentFolderPath -ChildPath "file_list.csv"

# Get all files recursively and export details to CSV
Get-ChildItem -Path $CurrentFolderPath -Recurse -File |
    Select-Object FullName, Name, LastWriteTime, Length |
    Export-Csv -Path $OutputCSV -NoTypeInformation -Encoding UTF8

Write-Host "File details saved to $OutputCSV"
