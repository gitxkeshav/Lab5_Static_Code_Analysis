# Lab5_Static_Code_Analysis
Static code analysis lab using Pylint, Bandit, and Flake8

Reflection – Lab 5: Static Code Analysis
1)Easiest vs Hardest Fixes: The easiest fix was changing the mutable default argument and replacing print statements with logging.
The hardest was rewriting the bare except: blocks — I had to figure out the right exceptions to catch without breaking the code.

2)False Positives:
Pylint flagged some harmless style issues like logging format warnings, and Flake8 complained about line lengths.
They didn’t really affect how the program ran.

3)Integration in Workflow:
I’d use these tools with GitHub Actions or pre-commit hooks so code gets checked automatically before pushing.
That way, errors and bad practices get caught early.

4)Improvements Seen: After fixing everything, the code feels cleaner, safer, and more reliable.
It now handles invalid inputs properly, uses better error handling, and logs everything neatly.


# Static Code Analysis Issues Table (Original `inventory_system.py`)

| **Issue** | **Type of Issue** | **Line(s)** | **Description** | **Fix Approach** |
|------------|------------------|--------------|-----------------|------------------|
| **Use of `eval()` (arbitrary code execution)** | Security Issue | 59 | The line `eval("print('eval used')")` allows arbitrary code execution, which is a major security vulnerability. | Removed `eval` entirely. Replaced with safe logging (`logger.info()`) or a direct print/function call. |
| **Bare `except:` (suppresses all errors)** | Error Handling Issue | 15–20 | The `removeItem` function uses `except:` with `pass`, which hides all exceptions. | Caught specific exceptions (like `KeyError`, `ValueError`) and logged unexpected errors instead of passing silently. |
| **Mutable default argument (`logs=[]`)** | Code Quality / Maintainability Issue | 11 | The mutable list `logs=[]` is shared across all calls, causing unintended data sharing between invocations. | Changed default to `None` and initialized inside the function (`if logs is None: logs = []`). |
| **No input validation (leads to TypeError)** | Logic / Data Validation Issue | 51–52 | Function `addItem(123, "ten")` passes wrong data types. Causes runtime `TypeError: int + str`. | Added `isinstance()` checks to ensure `item` is `str` and `qty` is `int` before performing arithmetic. |
| **File handling without context manager (`open()`)** | Resource Management Issue | 25–34 | Files opened using `open()` without `with` statement — risk of resource leaks and unclosed files. | Used context managers: `with open(file) as f:` for automatic close and better safety. |
| **Global variable misuse (`stock_data`)** | Design Issue | Multiple | Global variable is modified from multiple functions without thread safety or encapsulation. | Wrapped inventory logic in a class or encapsulated modification via functions; minimized global usage. |
| **No `__main__` guard** | Code Structure Issue | 58 | Script executes immediately upon import — not modular. | Added `if __name__ == "__main__": main()` at the end. |
| **Print statements instead of logging** | Code Quality / Maintainability Issue | 37, 38 | Raw `print()` statements are less flexible than structured logging. | Replaced `print()` with Python’s logging module (`logger.info()`). |

