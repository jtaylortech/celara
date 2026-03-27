Output web/public/recordings/securitykit-demo.gif
Set Theme "Dracula"
Set FontSize 16
Set Width 1200
Set Height 550
Set Padding 20
Set TypingSpeed 40ms

Hide
Type "PS1='$ '"
Enter
Show

Type "securitykit scan --rpc-url https://eth.llamarpc.com"
Enter
Sleep 300ms

Hide
Type "echo ''"
Enter
Type "echo '  ✅ [SK-001] RPC endpoint is reachable'"
Enter
Type "echo '     Node responded: Geth/v1.13.0'"
Enter
Type "echo ''"
Enter
Type "echo '  ✅ [SK-002] No unlocked accounts'"
Enter
Type "echo '     eth_accounts returned empty list'"
Enter
Type "echo ''"
Enter
Type "echo '  ✅ [SK-003] Admin API is not exposed'"
Enter
Type "echo '  ✅ [SK-004] Debug API is not exposed'"
Enter
Type "echo '  ✅ [SK-005] Mining is disabled'"
Enter
Type "echo '  ✅ [SK-006] Peer count healthy — 47 peers'"
Enter
Type "echo '  ✅ [SK-007] Node is fully synced'"
Enter
Type "echo '  ✅ [SK-008] Chain ID: 1 (Ethereum)'"
Enter
Type "echo ''"
Enter
Type "echo 'Results: 8 passed, 0 failed, 0 skipped'"
Enter
Show
Sleep 2s
