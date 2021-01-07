# YNAB-autoconverter

## Flow

0. Once in a day trigger program via Scheduler (if HEROKU)
1. Check config or environment for YNAB_TOKEN, BUDGET, ACC_NAMES, ASSETS
2. Validate parameters
3. Try to authorize
4. Get Budget ID based on BUDGET and YNAB_TOKEN
5. Get Accounts' ID based on ACC_NAMES
6. Get Accounts' first transaction memo
7. Get current rate for that Account's Asset
8. Calculate current value of Account and diff
9. Post transaction if value if absolute diff is > 0.5%
