import os
import sys
from pathlib import Path
print()
BASE_DIR = Path(__file__).resolve().parent.parent
print(BASE_DIR)
print()


for o in sys.path:
    print(o)