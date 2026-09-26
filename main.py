import sys
import os

# Tambahin folder project ke path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import fungsi main dari file bot
from rasyaprem_bot import main

if __name__ == "__main__":
    main()
