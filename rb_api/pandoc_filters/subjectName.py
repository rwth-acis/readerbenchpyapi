#!/usr/bin/env python3

import sys
import json

"""
Pandoc filter to convert all regular text to uppercase.
Code, link URLs, etc. are not affected.
"""
from panflute import run_filter, Str

def getJson(url):
    with open(url, encoding='UTF-8') as f:
        varData = json.load(f)
    return varData

def caps(elem, doc):
    if type(elem) == Str and elem.text == "-subject-":
        data = getJson('data.json')
        subject = data['subject'] +" Frage nummer "+data['question']
        elem.text = subject
        return elem

def main(doc=None):
    return run_filter(caps, doc=doc)

if __name__ == "__main__":
    main()