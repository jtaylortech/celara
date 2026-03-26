Output web/public/recordings/chainops-demo.gif
Set Theme "Dracula"
Set FontSize 14
Set Width 800
Set Height 500
Set Padding 20

Type "chainops init ethereum --network mainnet --region us-east-1"
Enter
Sleep 400ms
Type "✓ Configuration saved to chainops.yaml"
Enter
Sleep 500ms
Type ""
Enter
Type "chainops estimate"
Enter
Sleep 400ms
Type "┌─────────────────────────────┬──────────┐"
Enter
Type "│ Component                   │     Cost │"
Enter
Type "├─────────────────────────────┼──────────┤"
Enter
Type "│ EC2 Instance (t3.xlarge)    │  $120.00 │"
Enter
Type "│ EBS Storage (2TB gp3)       │  $160.00 │"
Enter
Type "│ Data Transfer (~500GB)      │   $45.00 │"
Enter
Type "│ CloudWatch                  │   $10.00 │"
Enter
Type "│ Total                       │  $335.00 │"
Enter
Type "└─────────────────────────────┴──────────┘"
Enter
Sleep 2s
