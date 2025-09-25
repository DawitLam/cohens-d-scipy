#!/usr/bin/env python3
"""
Windows-compatible Unicode test runner.
Uses proper encoding handling for Windows terminals.
"""

import os
import sys
import locale
import time

# Fix Windows Unicode issues
if sys.platform == 'win32':
 # Try to set UTF-8 encoding
 try:
 # For Windows 10 version 1903 and later
 os.system('chcp 65001 >nul 2>&1')
 except:
 pass

 # Set console encoding
 try:
 sys.stdout.reconfigure(encoding='utf-8', errors='replace')
 sys.stderr.reconfigure(encoding='utf-8', errors='replace')
 except:
 pass

# Fallback symbols for different terminals
class Symbols:
 def __init__(self):
 self.use_unicode = self._can_display_unicode()

 if self.use_unicode:
 self.check = "[PASS]"
 self.cross = "[FAIL]"
 self.arrow = ">>"
 self.rocket = ""
 self.party = ""
 self.warning = "[WARN]"
 else:
 self.check = "[PASS]"
 self.cross = "[FAIL]"
 self.arrow = ">>>"
 self.rocket = ">>>"
 self.party = "SUCCESS"
 self.warning = "WARNING"

 def _can_display_unicode(self):
 """Test if terminal can display Unicode."""
 try:
 print("[PASS]", end='', flush=True)
 print("\b\b ", end='', flush=True) # Erase the test character
 return True
 except UnicodeEncodeError:
 return False

# Global symbols instance
SYMBOLS = Symbols()

def safe_print(message):
 """Print message with encoding fallback."""
 try:
 print(message)
 except UnicodeEncodeError:
 # Fallback to ASCII
 ascii_message = message.encode('ascii', 'replace').decode('ascii')
 print(ascii_message)

def run_unicode_test():
 """Test if we can display Unicode properly."""
 safe_print(f"\n{SYMBOLS.arrow} Testing Unicode display capability...")
 safe_print(f"Unicode support: {'YES' if SYMBOLS.use_unicode else 'NO (using ASCII fallback)'}")
 safe_print(f"System encoding: {locale.getpreferredencoding()}")
 safe_print(f"Platform: {sys.platform}")

 if SYMBOLS.use_unicode:
 safe_print(f"{SYMBOLS.check} Unicode test: ✓ ")
 else:
 safe_print(f"{SYMBOLS.check} ASCII fallback mode active")

def main():
 """Test Unicode display and run basic validation."""
 safe_print("=" * 60)
 safe_print("UNICODE DISPLAY TEST FOR CROSS-PLATFORM COMPATIBILITY")
 safe_print("=" * 60)

 run_unicode_test()

 # Import and test the main package
 safe_print(f"\n{SYMBOLS.arrow} Testing Cohen's d package...")

 try:
 sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'cohens_d_package'))
 from cohens_d import cohens_d
 import numpy as np

 # Quick functionality test
 np.random.seed(42)
 x = np.random.normal(0, 1, 100)
 y = np.random.normal(0.5, 1, 100)
 result = cohens_d(x, y)

 safe_print(f"{SYMBOLS.check} Basic Cohen's d calculation: {result:.6f}")

 # Test multidimensional
 x_2d = np.random.normal(0, 1, (50, 10))
 y_2d = np.random.normal(0.3, 1, (50, 10))
 result_2d = cohens_d(x_2d, y_2d, axis=0)
 safe_print(f"{SYMBOLS.check} 2D array test: shape {result_2d.shape}")

 safe_print(f"\n{SYMBOLS.party} All tests completed successfully!")
 safe_print(f"{SYMBOLS.rocket} Your system can run Cohen's d validation tests!")

 return 0

 except Exception as e:
 safe_print(f"{SYMBOLS.cross} Test failed: {e}")
 return 1

if __name__ == "__main__":
 exit(main())