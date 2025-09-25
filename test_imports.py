#!/usr/bin/env python3
"""
Test script to validate import paths work correctly across different scenarios.
This helps verify that GitHub Actions will work properly.
"""

import sys
import os

def test_direct_import():
 """Test importing from the cohens_d_package directory."""
 print("Testing direct import from cohens_d_package...")
 try:
 sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'cohens_d_package'))
 from cohens_d import cohens_d
 import numpy as np

 # Quick test
 result = cohens_d(np.array([1, 2, 3]), np.array([2, 3, 4]))
 print(f"[PASS] Direct import works: d = {result:.3f}")
 return True
 except Exception as e:
 print(f"[FAIL] Direct import failed: {e}")
 return False

def test_installed_import():
 """Test importing from installed package (if available)."""
 print("\nTesting installed package import...")
 try:
 # Clear any previous imports
 if 'cohens_d' in sys.modules:
 del sys.modules['cohens_d']
 if 'cohens_d.core' in sys.modules:
 del sys.modules['cohens_d.core']

 # Try to import the installed package
 from cohens_d import cohens_d
 import numpy as np

 # Quick test
 result = cohens_d(np.array([1, 2, 3]), np.array([2, 3, 4]))
 print(f"[PASS] Installed package import works: d = {result:.3f}")
 return True
 except Exception as e:
 print(f"[FAIL] Installed package import failed: {e}")
 return False

def test_intensive_script_imports():
 """Test that intensive testing scripts can import properly."""
 print("\nTesting intensive testing script imports...")

 scripts = [
 'test_numerical_validation.py',
 'test_edge_cases.py',
 'test_performance.py',
 'test_multidimensional.py'
 ]

 success_count = 0
 for script in scripts:
 script_path = os.path.join('intensive_testing', script)
 try:
 # Run the import section of each script
 with open(script_path, 'r', encoding='utf-8') as f:
 content = f.read()

 # Extract and execute the import section
 lines = content.split('\n')
 import_lines = []
 for line in lines:
 if line.strip().startswith(('import ', 'from ', 'sys.path')):
 import_lines.append(line)
 elif 'class Test' in line:
 break

 import_code = '\n'.join(import_lines)
 exec(import_code, globals())

 print(f"[PASS] {script} imports work")
 success_count += 1

 except Exception as e:
 print(f"[FAIL] {script} imports failed: {e}")

 return success_count == len(scripts)

if __name__ == "__main__":
 print("=== Import Path Testing ===")

 results = []
 results.append(test_direct_import())
 results.append(test_installed_import())
 results.append(test_intensive_script_imports())

 print(f"\n=== Summary ===")
 print(f"Direct import: {'[PASS]' if results[0] else '[FAIL]'}")
 print(f"Installed import: {'[PASS]' if results[1] else '[FAIL]'}")
 print(f"Intensive scripts: {'[PASS]' if results[2] else '[FAIL]'}")

 if all(results):
 print("\n All import scenarios work correctly!")
 sys.exit(0)
 else:
 print("\n[WARN] Some import scenarios failed. GitHub Actions may have issues.")
 sys.exit(1)