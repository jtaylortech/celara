Output web/public/recordings/chainwatch-demo.gif
Set Theme "Dracula"
Set FontSize 16
Set Width 1200
Set Height 450
Set Padding 20
Set TypingSpeed 40ms

Hide
Type "PS1='$ '"
Enter
Show

Type "chainwatch exporter --chain ethereum --port 9100"
Enter
Sleep 300ms

Hide
Type "echo 'Starting ethereum exporter on port 9100'"
Enter
Type "echo 'Metrics at http://localhost:9100/metrics'"
Enter
Type "echo ''"
Enter
Show
Sleep 500ms

Type "curl -s localhost:9100/metrics | grep chainwatch"
Enter
Sleep 300ms

Hide
Type "echo 'chainwatch_sync_status    1.0'"
Enter
Type "echo 'chainwatch_current_block  19234567.0'"
Enter
Type "echo 'chainwatch_peer_count     47.0'"
Enter
Type "echo 'chainwatch_gas_price_gwei 12.34'"
Enter
Show
Sleep 2s
