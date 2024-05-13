$posh7 = "pwsh.exe" # PowerShell Core 7
$dir = $PSScriptRoot

$cmd = "& {
    wt new-tab -d $dir --title task3 ;
    wt new-tab -d $dir --title subscriber1 ;
    wt new-tab -d $dir --title subscriber2 ;
    wt new-tab -d $dir --title publisher ;
    wt new-tab -d $dir --title consumer1 ;
    wt new-tab -d $dir --title consumer2 ;
    wt new-tab -d $dir --title producer ;
}"

Start-Process -FilePath $posh7 -ArgumentList "-Command", $cmd