$posh7 = "pwsh.exe" # PowerShell Core 7
$dir = $PSScriptRoot

$cmd = "& {
    wt new-tab -d $dir --title client ;
    wt new-tab -d $dir --title facade ;
    wt new-tab -d $dir --title log1 ;
    wt new-tab -d $dir --title log2 ;
    wt new-tab -d $dir --title log3 ;
    wt new-tab -d $dir --title msg1 ;
}"

Start-Process -FilePath $posh7 -ArgumentList "-Command", $cmd