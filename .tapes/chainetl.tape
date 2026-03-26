Output web/public/recordings/chainetl-demo.gif
Set Theme "Dracula"
Set FontSize 14
Set Width 800
Set Height 500
Set Padding 20

Type "chainetl sync --chain ethereum --start-block 18000000 --count 5 --destination jsonl"
Enter
Sleep 500ms
Type "Syncing blocks 18000000 to 18000004 (5 blocks)"
Enter
Sleep 300ms
Type "Extracting blocks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5/5"
Enter
Sleep 200ms
Type "Loaded 5 blocks"
Enter
Type "Checkpoint saved at block 18000004"
Enter
Sleep 1s

Type "cat output/ethereum_blocks.jsonl | jq '.number'"
Enter
Sleep 300ms
Type "18000000"
Enter
Type "18000001"
Enter
Type "18000002"
Enter
Type "18000003"
Enter
Type "18000004"
Enter
Sleep 2s
