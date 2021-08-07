  
#!/usr/bin/env python3



"""
Replace Emph elements with Strikeout elements
"""

from pandocfilters import toJSONFilter, Str


def caps(key, value, format, meta):
    if key == 'Str':
        return Str(value.upper())

if __name__ == "__main__":
    toJSONFilter(caps)