# Issues Found - Bank Account System

**Name:** Akshat Sharma
**SRN:** PES1UG24CS042

Tools used: Pylint, Bandit, Flake8. Line numbers are from the original file.

Scores before: Pylint 5.62/10, Bandit 6 issues (2 High, 1 Medium, 3 Low), Flake8 7 issues
Scores after: Pylint 10.00/10, Bandit 0 issues, Flake8 0 issues

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command injection (B605) | Security (High) | 55 | `os.system("echo Backup complete: " + filename)` runs a shell with the filename joined in, so a filename like `x; del *` would run extra commands | Removed `os.system` and just used `print()` for the message |
| Weak MD5 hash (B324) | Security (High) | 44 | PIN was hashed with MD5 which is broken and easy to crack | Changed to `hashlib.sha256` |
| Use of eval (B307 / W0123) | Security (Medium) | 39 | `compute_bonus` ran `eval(expr)` on a string, any code passed in would get executed | Changed the function to take a numeric `rate` and return `bal * rate` |
| Try/except/pass + bare except (B110 / W0702 / E722) | Security / Bug (Low) | 22-23 | Deposit to a wrong account id failed silently, and bare except also catches things like KeyboardInterrupt | Catch only `KeyError`, print an error and return False |
| Hardcoded secret token (B105) | Security (Low) | 59, 67 | Admin token was written in the source code and also printed to the console | Read it from the `BANK_ADMIN_TOKEN` environment variable and don't print its value |
| Insecure random for PIN (B311) | Security (Low) | 48 | `random.randint` is predictable, not ok for PINs | Used `secrets.randbelow(9000) + 1000` |
| Service fee never charged (F841 / W0612) | Bug (logic) | 27 | `service_fee = 2.50` was declared but never subtracted, so withdrawals were free. Output balance was 1300 instead of 1297.5 | Made it a constant `SERVICE_FEE` and subtract `amount + SERVICE_FEE` (also check balance covers both) |
| Mutable default argument (W0102) | Bug | 11 | `transactions=[]` is the same list shared across every call | Default to `None` and create a new list inside the function |
| Unused import (F401 / W0611) | Style | 6 | `sys` was imported but not used | Removed the import |
| Comparison to None (E711 / C0121) | Style | 28 | Used `== None` | Changed to `is None` |
| Unused variable `bal` (F841 / W0612) | Style | 38 | `bal` was only used inside the eval string so tools saw it as unused | Fixed along with the eval change, `bal` is used directly now |
| File not closed safely (R1732 / W1514) | Bug / Style | 52-54 | `open()` without `with` and without encoding, file stays open if write fails | Used `with open(filename, "w", encoding="utf-8")` |
| Line too long (E501) | Style | 15 | Line was 89 characters (limit 79) | Split the string across two lines |
| No newline at end of file (W292 / C0304) | Style | 70 | Missing final newline | Added newline at end |
| Function name not snake_case (C0103) | Style | 11 | `createAccount` is camelCase | Renamed to `create_account` |
| Old style % formatting (C0209) | Style | 15 | Used `%` string formatting | Changed to f-string |
| Unnecessary else after return (R1705) | Style | 32 | `else` after a `return` is not needed | Removed the else and de-indented |
| Missing docstrings (C0116) | Style | 11, 19, 26, 37, 43, 47, 51, 58 | Functions had no docstrings | Added short docstrings to every function |

Other small change: `main()` is now called inside `if __name__ == "__main__":` so importing the file doesn't run the demo.

## Commits

1. Bandit fixes (all security issues)
2. Flake8 fixes (style + the service fee bug)
3. Pylint fixes (naming, docstrings, mutable default, with-open etc.)

Before reports are in `*_report_before.txt` and after reports are in `*_report.txt`. The final `flake8_report.txt` is empty because flake8 prints nothing when there are no issues.
