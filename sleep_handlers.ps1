param([string]$Action)

try {
    if ($Action -eq "sleep") {
        Invoke-RestMethod -Uri "https://api.telegram.org/bot8774485792:AAF9G8BIi47uXvuhtXxILUluGzQdd3-Cl8E/sendMessage" -Method Post -ContentType "application/json" -Body '{"chat_id":7699121205,"text":"/sleep"}' -UseBasicParsing -ErrorAction Stop | Out-Null
    } elseif ($Action -eq "wake") {
        Invoke-RestMethod -Uri "https://api.telegram.org/bot8774485792:AAF9G8BIi47uXvuhtXxILUluGzQdd3-Cl8E/sendMessage" -Method Post -ContentType "application/json" -Body '{"chat_id":7699121205,"text":"/online"}' -UseBasicParsing -ErrorAction Stop | Out-Null
    }
} catch {}