# Reflection – Lab 5: Static Code Analysis

1)Easiest vs Hardest Fixes: 
The easiest fix was changing the mutable default argument and replacing print statements with logging.  
The hardest was rewriting the bare `except:` blocks — I had to figure out the right exceptions to catch without breaking the code.

2)False Positives:  
Pylint flagged some harmless style issues like logging format warnings, and Flake8 complained about line lengths.  
They didn’t really affect how the program ran.

3)Integration in Workflow:  
I’d use these tools with GitHub Actions or pre-commit hooks so code gets checked automatically before pushing.  
That way, errors and bad practices get caught early.

4)Improvements Seen:
After fixing everything, the code feels cleaner, safer, and more reliable.  
It now handles invalid inputs properly, uses better error handling, and logs everything neatly.
