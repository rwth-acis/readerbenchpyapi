#!/usr/bin/env python3


import json

"""
Pandoc filter to convert all regular text to uppercase.
Code, link URLs, etc. are not affected.
"""
import pygraphviz
import hashlib
import os
import sys
from pandocfilters import toJSONFilter, Str, Para, Image

imagedir = "rb_api/output/figures"

def getJson(url):
    with open(url, encoding='UTF-8') as f:
        varData = json.load(f)
    return varData

def caps(key, value, format, meta):
    if key == 'Str' and value == "-graph1-":
        data = getJson('data.json')
        caption = "caption"
        if format == "html":
            filetype = "png"
        elif format == "latex":
            filetype = "pdf"
        else:
            filetype = "png"
        alt = Str(caption)
        src = 'rb_api/output/figures' + '/' + 'wordnet' + '.' + 'png'
        tit = ""
        return Para([Image(['', [], []], [alt], [src, tit])]) 

if __name__ == "__main__":
    toJSONFilter(caps)
    sys.stdout.flush()