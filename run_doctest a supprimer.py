import doctest
import importlib.util
import sys
from pathlib import Path

# ANSI colors
GREEN = "\033[92m"
RED = "\033[91m"
RESET = "\033[0m"

def run_file(path):
    spec = importlib.util.spec_from_file_location("mod", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    result = doctest.testmod(mod, verbose=False)

    if result.failed == 0:
        print(f"{GREEN}✔ PASS{RESET} {path}")
    else:
        print(f"{RED}✘ FAIL ({result.failed} failures){RESET} {path}")

if __name__ == "__main__":
    for file in sys.argv[1:]:
        run_file(file)
