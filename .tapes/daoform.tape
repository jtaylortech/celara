Output web/public/recordings/daoform-demo.gif
Set Theme "Dracula"
Set FontSize 14
Set Width 800
Set Height 450
Set Padding 20

Type "daoform init --name MyDAO"
Enter
Sleep 400ms
Type "Created dao.yaml for 'MyDAO'"
Enter
Type "  Quorum: 10.0%"
Enter
Type "  Threshold: 50.0%"
Enter
Type "  Voting period: 7 days"
Enter
Sleep 500ms
Type ""
Enter
Type "daoform validate"
Enter
Sleep 300ms
Type "✅ Valid config for 'MyDAO'"
Enter
Sleep 500ms
Type ""
Enter
Type "daoform propose --id PROP-1 --title 'Fund core dev' --author alice.eth"
Enter
Sleep 300ms
Type "Created proposal: PROP-1"
Enter
Type "  Title: Fund core dev"
Enter
Type "  Status: draft"
Enter
Sleep 2s
