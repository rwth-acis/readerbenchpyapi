#!/usr/bin/env python3

import sys
import json
import os

"""
Pandoc filter to convert all regular text to uppercase.
Code, link URLs, etc. are not affected.
"""
from panflute import run_filter, Str, Para, Image

def getJson(url):
    with open(url, encoding='UTF-8') as f:
        varData = json.load(f)
    return varData

def caps(elem, doc):
    data = getJson('data.json')
    if type(elem) == Str: 
        if elem.text == "-topicName-":
            subject = data['subject'] +" Frage nummer " + str(data['questionNumber'])
            elem.text = subject
            return elem
        if elem.text == "-feedback-":
            feedback = data[data['subject']+str(data['questionNumber'])]
            elem.text = feedback
            return elem
        if elem.text == "-expert-":
            caption = "caption"
            src = 'rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_expert_keyword.png'
            alt = Str(caption)

            if not os.path.isfile('rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_expert_keyword.png'):
                return None

            return Image(alt, url=src, title='')
        if elem.text == "-student-":
            caption = "caption"
            src = 'rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_keyword.png'
            alt = Str(caption)

            if not os.path.isfile('rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_keyword.png'):
                return None

            return Image(alt, url=src, title='')

        if elem.text == "-cohesion-":
            caption = "caption"
            src = 'rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_cna.png'
            alt = Str(caption)

            if not os.path.isfile('rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_cna.png'):
                return None

            return Image(alt, url=src, title='')
            
def main(doc=None):
    return run_filter(caps, doc=doc)

if __name__ == "__main__":
    main()