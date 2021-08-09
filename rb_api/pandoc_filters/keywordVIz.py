#!/usr/bin/env python3


"""
 Filtering function. The filtering of the target format docx is in this filtering function.
"""
import os
import sys
from subprocess import Popen, PIPE, call

from panflute import toJSONFilter, Str, Para, Image, CodeBlock
import json

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

    if elem.text == "-graph1-":
        caption = "caption"
        src = 'rb_api/output/figures/04.png'
        imgPath  = 'rb_api/output/figures/04.png'
        alt = Str(caption)

        if not os.path.isfile(dest):
            return None

        return Image(alt, url=src, title='')


def main(doc=None):
    return run_filter(caps, doc=doc)

if __name__ == "__main__":
    main()