# tests/conftest.py
import sys
import os

# Add the project root directory and the fwoptimizer directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../fwoptimizer')))