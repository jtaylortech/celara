Output web/public/recordings/chainwatch-demo.gif
Set Theme "Dracula"
Set FontSize 14
Set Width 800
Set Height 450
Set Padding 20

Type "chainwatch exporter --chain ethereum --port 9100"
Enter
Sleep 400ms
Type "Starting ethereum exporter on port 9100"
Enter
Type "Metrics at http://localhost:9100/metrics"
Enter
Sleep 500ms
Type ""
Enter
Type "curl -s localhost:9100/metrics | grep chainwatch"
Enter
Sleep 300ms
Type "chainwatch_sync_status{chain='ethereum'} 1.0"
Enter
Sleep 150ms
Type "chainwatch_current_block{chain='ethereum'} 19234567.0"
Enter
Sleep 150ms
Type "chainwatch_peer_count{chain='ethereum'} 47.0"
Enter
Sleep 150ms
Type "chainwatch_gas_price_gwei{chain='ethereum'} 12.34"
Enter
Sleep 2s
