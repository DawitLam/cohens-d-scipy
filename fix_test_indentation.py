#!/usr/bin/env python3
"""
Script to completely fix the test file indentation issues.
"""

import re

def fix_test_file():
    """Fix all indentation issues in the test file."""
    file_path = r"c:\Users\Dama\Documents\Cohen D\cohens_d_package\tests\test_cohens_d.py"
    
    # Read the original file
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines and track indentation context
    lines = content.split('\n')
    fixed_lines = []
    indent_stack = [0]  # Stack to track current indentation level
    
    for i, line in enumerate(lines):
        stripped = line.strip()
        
        # Skip empty lines
        if not stripped:
            fixed_lines.append('')
            continue
        
        # Determine the correct indentation level
        current_indent = get_correct_indentation(stripped, fixed_lines, indent_stack)
        
        # Apply the correct indentation
        fixed_lines.append(' ' * current_indent + stripped)
    
    # Write the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))
    
    print(f"Fixed {file_path}")

def get_correct_indentation(line, previous_lines, indent_stack):
    """Determine the correct indentation for a line."""
    
    # Class definitions - no indentation
    if line.startswith('class '):
        indent_stack[:] = [0]
        return 0
    
    # Top-level function definitions - no indentation  
    if line.startswith('def ') and not any('class ' in prev for prev in previous_lines[-10:] if prev.strip()):
        indent_stack[:] = [0]
        return 0
    
    # Method definitions inside classes - 4 spaces
    if line.startswith('def '):
        indent_stack[:] = [4]
        return 4
    
    # Look at the last non-empty line
    last_line = None
    for prev_line in reversed(previous_lines):
        if prev_line.strip():
            last_line = prev_line
            break
    
    if not last_line:
        return 0
    
    last_indent = len(last_line) - len(last_line.lstrip())
    last_stripped = last_line.strip()
    
    # Special cases that decrease indentation
    if line in ['else:', 'elif ', 'except:', 'except ', 'finally:'] or line.startswith('elif ') or line.startswith('except '):
        return max(0, last_indent - 4)
    
    # Lines that should be at the same level as the previous
    if line.startswith(('@', 'import ', 'from ', 'class ', 'def ')):
        return 0 if line.startswith(('class ', 'def ')) else last_indent
    
    # Lines that should be indented more than the previous
    if last_stripped.endswith(':'):
        return last_indent + 4
    
    # Context managers, try blocks, etc.
    if any(last_stripped.startswith(kw) for kw in ['with ', 'try:', 'if ', 'elif ', 'else:', 'for ', 'while ', 'def ', 'class ']):
        return last_indent + 4
    
    # Default: same indentation as previous line
    return last_indent

if __name__ == "__main__":
    fix_test_file()