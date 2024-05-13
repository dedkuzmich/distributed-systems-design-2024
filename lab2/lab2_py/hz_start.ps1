$numMembers = 3
$posh7 = "pwsh.exe" # PowerShell Core 7

# Start Hazelcast members
for ($i = 1; $i -le $numMembers; $i++)
{
    # Run .bat script
    $cmd = "& {
    hz-start.bat;
    }"

    Start-Process -FilePath $posh7 -ArgumentList "-Command", $cmd
}
