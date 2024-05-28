$posh7 = "pwsh.exe" # PowerShell Core 7
$dir = $PSScriptRoot

$cmd = "& {
    wt new-tab -d $dir/client --title client1 ;
    wt new-tab -d $dir/client --title client2 ;
    wt new-tab -d $dir --title master ;
    wt new-tab -d $dir --title sec1 ;
    wt new-tab -d $dir --title sec2 ;
}"

Start-Process -FilePath $posh7 -ArgumentList "-Command", $cmd