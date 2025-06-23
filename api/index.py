# Entrypoint for Vercel serverless deployment
# This is your Main.py, adapted for Vercel

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Main import app as application
