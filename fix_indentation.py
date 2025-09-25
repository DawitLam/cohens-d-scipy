#!/usr/bin/env python3
"""
Script to fix Python indentation issues caused by icon replacement.
"""

import re

def fix_python_indentation(file_path):
    """Fix indentation in a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into lines
    lines = content.split('\n')
    fixed_lines = []
    
    for i, line in enumerate(lines):
        # Skip empty lines
        if not line.strip():
            fixed_lines.append(line)
            continue
            
        # Check if line starts with spaces (broken indentation)
        if line.startswith(' ') and not line.startswith('    ') and not line.startswith('  '):
            # This is a broken indentation line - fix it
            stripped = line.lstrip()
            
            # Determine proper indentation based on context
            if any(keyword in stripped for keyword in ['def ', 'class ', 'if ', 'elif ', 'else:', 'for ', 'while ', 'try:', 'except ', 'finally:', 'with ']):
                # Top-level or first level statements
                if stripped.startswith('def ') or stripped.startswith('class '):
                    fixed_lines.append(stripped)  # No indentation for top-level
                else:
                    # These should be indented based on context
                    # Look back to find the proper indentation level
                    proper_indent = get_proper_indentation(fixed_lines, stripped)
                    fixed_lines.append(proper_indent + stripped)
            else:
                # Regular code lines - determine indentation from context
                proper_indent = get_proper_indentation(fixed_lines, stripped)
                fixed_lines.append(proper_indent + stripped)
        else:
            # Line has proper indentation or no indentation
            fixed_lines.append(line)
    
    # Write back the fixed content
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(fixed_lines))

def get_proper_indentation(previous_lines, current_line):
    """Determine the proper indentation for the current line."""
    if not previous_lines:
        return ''
    
    # Look at the last non-empty line
    for line in reversed(previous_lines):
        if line.strip():
            last_line = line
            break
    else:
        return ''
    
    # Count indentation of last line
    last_indent = len(last_line) - len(last_line.lstrip())
    
    # Determine if we should indent more
    if last_line.rstrip().endswith(':'):
        # Previous line ended with colon, indent more
        return ' ' * (last_indent + 4)
    elif any(current_line.startswith(keyword) for keyword in ['return ', 'break', 'continue', 'pass', 'raise ']):
        # Control flow statements typically at current level
        return ' ' * last_indent
    elif current_line.startswith('"""') or current_line.startswith("'''"):
        # Docstrings typically at same level as function
        return ' ' * last_indent
    else:
        # Regular statements - same level as previous
        return ' ' * last_indent

if __name__ == "__main__":
    file_path = r"c:\Users\Dama\Documents\Cohen D\cohens_d_package\cohens_d\core.py"
    fix_python_indentation(file_path)
    print(f"Fixed indentation in {file_path}")