# Reflection - Lab 5 Static Code Analysis

**Name:** Akshat Sharma
**SRN:** PES1UG24CS042

### 1. Which issues were the easiest to fix, and which were the hardest? Why?

The easiest ones were the Flake8 style issues like the unused `sys` import, missing newline at the end, `== None` and the long line. The report tells you the exact line and what to change, so these took a few seconds each. Missing docstrings and renaming `createAccount` were also easy, I just had to remember to rename the call in `main()` too.

The harder ones were the security issues from Bandit because I couldn't just delete the line, I had to change how the function works. For `eval()` I had to decide what `compute_bonus` was actually supposed to do and change it to take a rate instead of a string expression. For the hardcoded token I had to think about where the token should come from (environment variable) and also stop printing it. The service fee bug was also tricky because the tool only said "unused variable". If I had just deleted the variable the warning would go away but the bug (no fee being charged) would still be there.

### 2. Did the static analysis tools report any false positives? If so, describe one example.

Kind of. Pylint and Flake8 said `bal` in `compute_bonus` was unused, but it was actually being used inside the string passed to `eval()`. The tools can't see inside strings so they flagged it. It wasn't really a wrong warning though, it was pointing to the eval problem.

Bandit's B105 (hardcoded password) works by matching the variable name and string, so it could flag normal strings that aren't secrets. In this file it was correct since the token really was a secret. Also some of the Pylint style warnings like missing docstrings don't affect how the program runs, they are more about readability.

### 3. How would you integrate static analysis tools into your actual software development workflow?

- Run flake8 and pylint in the editor (VS Code extensions) so problems show up while typing.
- Add a pre-commit hook that runs flake8 and bandit so bad code can't be committed easily.
- In GitHub Actions, run all three tools on every push / pull request and fail the build if Bandit finds Medium/High issues or the Pylint score goes below something like 9.
- Keep a config file (`.pylintrc` / `setup.cfg`) in the repo so everyone on the team uses the same rules.

### 4. What tangible improvements did you observe in the code quality, readability, or potential robustness after applying the fixes?

- Pylint score went from 5.62 to 10.00, Bandit went from 6 issues to 0 and Flake8 from 7 to 0.
- Security is a lot better: no more `eval`, no shell command, no secret in the code, SHA-256 instead of MD5 and `secrets` instead of `random`.
- Found and fixed an actual bug: the withdrawal service fee was never charged. Balance is now 1297.5 instead of 1300.
- Errors don't get hidden anymore. Depositing to a wrong account now prints a message and returns False instead of silently doing nothing.
- The mutable default fix means transactions from different calls won't mix together.
- Docstrings and snake_case names make the code easier to read, and using `with open` means the backup file is always closed properly.
