#!/usr/bin/env python3

import sys
import json
import os

"""
Pandoc filter to convert all regular text to uppercase.
Code, link URLs, etc. are not affected.
"""
from panflute import run_filter, Str, Para, Image, DefinitionList, BulletList, ListItem, Strong
import panflute as pf

def getJson(url):
    with open(url, encoding='UTF-8') as f:
        varData = json.load(f)
    return varData



def caps(elem, doc):
    data = getJson('data.json')
    if isinstance(elem, pf.RawBlock) and (elem.format == 'html'):
        if elem.text == "<!-- feedback -->":
            feedback = data[data['subject']+str(data['questionNumber'])]
            body = []
            i=0
            for item in feedback:
                cells = [str(i+1),item]
                cells = [pf.TableCell(pf.Plain(Str(cell))) for cell in cells]
                row = pf.TableRow(*cells)
            
                body.append(pf.TableBody(row))
                i=i+1

            cells = ['Nr.','Empfehlung']
            cells = [pf.TableCell(pf.Plain(Str(cell))) for cell in cells]
            row = pf.TableRow(*cells)
            head = pf.TableHead(row)

            width = [0.1,0.7]
            alignment = ['AlignDefault'] * len(width)
            caption = 'Empfehlungen'
            caption = pf.Caption(Para(Str(caption)))
            return pf.Div(pf.Table(*body, colspec=zip(alignment, width), caption=caption))
        
        if elem.text == "<!-- textelementen -->":
            subject = data[data['subject']+str(data['questionNumber'])+'_cna']
            body = []
            i=0
            for item in subject:
                cells = [item[0], item[1]]
                cells = [pf.TableCell(pf.Plain(Str(cell))) for cell in cells]
                row = pf.TableRow(*cells)
            
                body.append(pf.TableBody(row))
                i=i+1

            cells = ['Abschnitt','Wert']
            cells = [pf.TableCell(pf.Plain(Str(cell))) for cell in cells]
            row = pf.TableRow(*cells)
            head = pf.TableHead(row)

            width = [0.16,0.7]
            alignment = ['AlignDefault'] * len(width)
            caption = 'Textelementen'
            caption = pf.Caption(Para(Str(caption)))
            return pf.Div(pf.Table(*body, colspec=zip(alignment, width), caption=caption))

    if type(elem) == Str: 
        if elem.text == "-topicName-":
            subject = data['subject'] +" Frage nummer " + str(data['questionNumber'])
            elem.text = subject
            return elem
        
        if elem.text == "-textelementen-":
            subject = data[data['subject']+str(data['questionNumber'])+'_cna']
            elem.text = subject
            return elem
        
        if elem.text == "-question_number-":
            feedback = str(data['questionNumber'])
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

        if elem.text == "-content-":
            caption = "caption"
            src = 'rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_cna_content.png'
            alt = Str(caption)

            if not os.path.isfile('rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_cna_content.png'):
                return None

            return Image(alt, url=src, title='')
        
        if elem.text == "-topic-":
            caption = "caption"
            src = 'rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_cna_topic.png'
            alt = Str(caption)

            if not os.path.isfile('rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_cna_topic.png'):
                return None

            return Image(alt, url=src, title='')

        if elem.text == "-argument-":
            caption = "caption"
            src = 'rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_cna_argument.png'
            alt = Str(caption)

            if not os.path.isfile('rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_cna_argument.png'):
                return None

            return Image(alt, url=src, title='')
        
        if elem.text == "-wordtovec-":
            caption = "caption"
            src = 'rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_cna_word2vec.png'
            alt = Str(caption)

            if not os.path.isfile('rb_api/pandoc_filters/images/'+data['subject']+str(data['questionNumber'])+'_cna_word2vec.png'):
                return None

            return Image(alt, url=src, title='')
            
def main(doc=None):
    return run_filter(caps, doc=doc)

if __name__ == "__main__":
    main()