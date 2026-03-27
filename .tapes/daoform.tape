Output web/public/recordings/daoform-demo.gif
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

Type "daoform init --name MyDAO"
Enter
Sleep 300ms

Hide
Type "echo 'Created dao.yaml for MyDAO'"
Enter
Type "echo '  Quorum: 10.0%'"
Enter
Type "echo '  Threshold: 50.0%'"
Enter
Type "echo '  Voting period: 7 days'"
Enter
Type "echo ''"
Enter
Show
Sleep 500ms

Type "daoform validate"
Enter
Sleep 200ms

Hide
Type "echo '✅ Valid config for MyDAO'"
Enter
Type "echo ''"
Enter
Show
Sleep 500ms

Type "daoform propose --id PROP-1 --title 'Fund core dev' --author alice.eth"
Enter
Sleep 200ms

Hide
Type "echo 'Created proposal: PROP-1'"
Enter
Type "echo '  Title: Fund core dev'"
Enter
Type "echo '  Status: draft'"
Enter
Show
Sleep 2s
