#!/usr/bin/env python3
"""
Script to remove emoji icons from all project files and replace them with text alternatives.
"""

import os
import re
import glob

# Define icon replacements
ICON_REPLACEMENTS = {
 '[PASS]': '[PASS]',
 '[FAIL]': '[FAIL]',
 '>>': '>>',
 '': '',
 '': '',
 '': '',
 '': '',
 '': '',
 '': '',
 '': '',
 '[ERROR]': '[ERROR]',
 '': '',
 '[WARN]': '[WARN]',
 # Additional icons found
 '': '',
 '': '',
 '': '',
 '': '',
}

def remove_icons_from_file(filepath):
 """Remove icons from a single file."""
 try:
 with open(filepath, 'r', encoding='utf-8') as f:
 content = f.read()

 original_content = content

 # Replace each icon
 for icon, replacement in ICON_REPLACEMENTS.items():
 content = content.replace(icon, replacement)

 # Clean up any double spaces or awkward spacing
 content = re.sub(r' +', ' ', content) # Multiple spaces to single space
 content = re.sub(r' +\n', '\n', content) # Trailing spaces before newlines

 # Only write if content changed
 if content != original_content:
 with open(filepath, 'w', encoding='utf-8') as f:
 f.write(content)
 print(f"Updated: {filepath}")
 return True
 else:
 print(f"No changes: {filepath}")
 return False

 except Exception as e:
 print(f"Error processing {filepath}: {e}")
 return False

def main():
 """Main function to process all relevant files."""
 base_dir = "c:\\Users\\Dama\\Documents\\Cohen D"

 # File patterns to process
 file_patterns = [
 os.path.join(base_dir, "*.py"),
 os.path.join(base_dir, "*.md"),
 os.path.join(base_dir, "*.sh"),
 os.path.join(base_dir, "intensive_testing", "*.py"),
 os.path.join(base_dir, "cohens_d_package", "**", "*.py"),
 ]

 updated_files = []

 for pattern in file_patterns:
 files = glob.glob(pattern, recursive=True)
 for filepath in files:
 if os.path.isfile(filepath):
 if remove_icons_from_file(filepath):
 updated_files.append(filepath)

 print(f"\nSummary: Updated {len(updated_files)} files")
 for filepath in updated_files:
 print(f" - {os.path.relpath(filepath, base_dir)}")

 return len(updated_files)

if __name__ == "__main__":
 updated_count = main()
 print(f"\nIcon removal complete. {updated_count} files updated.")