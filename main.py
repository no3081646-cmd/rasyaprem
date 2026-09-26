# File ini cuma buat jalanin bot
# Railway butuh entry point bernama main.py

import os
import sys

# Jalanin file bot
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from rasyaprem_bot import main

if __name__ == "__main__":
    main()
