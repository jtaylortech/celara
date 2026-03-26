Output web/public/recordings/chainetl-demo.gif
Set Theme "Dracula"
Set FontSize 14
Set Width 800
Set Height 500
Set Padding 20
Set TypingSpeed 40ms

Hide
Type "PS1='$ '"
Enter
Show

Type "chainetl sync --chain ethereum --start-block 18000000 --count 5 --destination jsonl"
Enter
Sleep 300ms

Hide
Type "echo ''"
Enter
Type "echo 'Syncing blocks 18000000 to 18000004 (5 blocks)'"
Enter
Type "echo 'Extracting blocks ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5/5'"
Enter
Type "echo 'Loaded 5 blocks'"
Enter
Type "echo 'Checkpoint saved at block 18000004'"
Enter
Show
Sleep 1s

Type "cat output/ethereum_blocks.jsonl | jq '.number'"
Enter

Hide
Type "echo '18000000'"
Enter
Type "echo '18000001'"
Enter
Type "echo '18000002'"
Enter
Type "echo '18000003'"
Enter
Type "echo '18000004'"
Enter
Show
Sleep 2s
