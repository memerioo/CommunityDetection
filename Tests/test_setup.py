import os
import sys

# This adds the 'scripts' directory to the path
base_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
scripts_path = os.path.join(base_directory, 'scripts')
sys.path.insert(0, scripts_path)

print("Scripts path added to sys.path:", scripts_path)
