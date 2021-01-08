# YNAB-autoconverter

## Flow

Once in a day trigger script via `Scheduler` (if `HEROKU`)
1. Check config or environment for `YNAB_TOKEN`, `CCAPI_TOKEN`
2. Parse parameters
3. Get Budgets based on `YNAB_TOKEN`
4. Get Accounts based on Budgets
5. Parse Account's notes
6. Get current rate for Account's asset
7. Calculate current value of Account's asset and diff
8. Post transaction if `abs(diff) > 0.5%`

## Executing
- install `python3.8`
- Either:
    - create environment variables `YNAB_TOKEN` and `CCAPI_TOKEN` with corresponding values
    - create `CONFIG.cfg` in `main.py`'s directory as in [example](#config-file-structure)
- `pip install -r requitements.txt`
- `python main.py`

## API Tokens

### Currency Converter API Token
Claim [here](https://free.currencyconverterapi.com/) (free) via email.

### You Need A Budget API Token
Claim [here](https://app.youneedabudget.com/settings/developer) via YNAB accound
(paid subscription except trial or college).

## Config file structure
```
[COMMON]
YNAB_TOKEN=<YNAB_TOKEN>
CCAPI_TOKEN=<CCAPI_TOKEN>
```
## License
License available at [LICENSE.md](LICENSE.md)
