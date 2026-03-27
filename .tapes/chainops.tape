Output web/public/recordings/chainops-demo.gif
Set Theme "Dracula"
Set FontSize 16
Set Width 1200
Set Height 500
Set Padding 20
Set TypingSpeed 40ms

Hide
Type "PS1='$ '"
Enter
Show

Type "chainops init ethereum --network mainnet --region us-east-1"
Enter
Sleep 300ms

Hide
Type "echo 'Initializing ethereum validator on mainnet...'"
Enter
Type "echo '✓ Configuration saved to chainops.yaml'"
Enter
Type "echo ''"
Enter
Show
Sleep 500ms

Type "chainops estimate"
Enter
Sleep 300ms

Hide
Type "echo '┌─────────────────────────────┬──────────┐'"
Enter
Type "echo '│ Component                   │     Cost │'"
Enter
Type "echo '├─────────────────────────────┼──────────┤'"
Enter
Type "echo '│ EC2 Instance (t3.xlarge)    │  \$120.00 │'"
Enter
Type "echo '│ EBS Storage (2TB gp3)       │  \$160.00 │'"
Enter
Type "echo '│ Data Transfer (~500GB)      │   \$45.00 │'"
Enter
Type "echo '│ CloudWatch                  │   \$10.00 │'"
Enter
Type "echo '│ Total                       │  \$335.00 │'"
Enter
Type "echo '└─────────────────────────────┴──────────┘'"
Enter
Show
Sleep 2s
