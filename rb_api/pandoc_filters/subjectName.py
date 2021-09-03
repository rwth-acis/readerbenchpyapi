#!/usr/bin/env python3

import sys
import json
import os
import itertools

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

def divide_chunks(l, n):
    	
	# looping till length l
	for i in range(0, len(l), n):
		yield l[i:i + n]

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

            cells = ['Abschnitt','Schlusselwörter']
            cells = [pf.TableCell(pf.Plain(Str(cell))) for cell in cells]
            row = pf.TableRow(*cells)
            head = pf.TableHead(row)

            width = [0.16,0.7]
            alignment = ['AlignDefault'] * len(width)
            caption = 'Textelementen'
            caption = pf.Caption(Para(Str(caption)))
            return pf.Div(pf.Table(*body, colspec=zip(alignment, width), caption=caption))

        if elem.text == "<!-- unterschied -->":
            expert = data[data['subject']+str(data['questionNumber'])+'_expert_keyword']
            student = data[data['subject']+str(data['questionNumber'])+'_keyword']
            sorted_expert = sorted(expert, key = lambda k:k['degree'])
            sorted_student = sorted(student, key = lambda k:k['degree'])
            unterschied = []
            for e in expert:
                unterschied.append(e["displayName"]+"("+str(round(float(e["degree"])*100, 2))+")")
                
            for e in expert:
                inside = True
                for s in student:
                    if e['displayName'] == s['displayName']:
                        inside= False
                        break
                if not inside:
                    unterschied.append(e["displayName"]+"("+str(round(float(e["degree"])*100, 2))+")")
                
                break
            string =''
            if len(unterschied) == 1:
                string+= str(unterschied[0])
            elif len(unterschied)>1:
                string = unterschied[0]
                for index in range(1, len(unterschied)-1): 
                    string +=', '+ str(unterschied[index])

            body = []
            
            cells = [string]
            cells = [pf.TableCell(pf.Plain(Str(cell))) for cell in cells]
            row = pf.TableRow(*cells)
        
            body.append(pf.TableBody(row))
                

            

            width = [0.8]
            alignment = ['AlignDefault'] * len(width)
            caption = 'Textelementen'
            caption = pf.Caption(Para(Str(caption)))
            return pf.Div(pf.Table(*body, colspec=zip(alignment, width), caption=caption))


        if elem.text == "- gemeinsam -":
            expert = data[data['subject']+str(data['questionNumber'])+'_expert_keyword']
            student = data[data['subject']+str(data['questionNumber'])+'_keyword']
            sorted_expert = sorted(expert, key = lambda k:k['degree'])
            sorted_student = sorted(student, key = lambda k:k['degree'])
            gemeinsam = []
            for e in expert:
                for s in student:
                    if e['displayName'] == s['displayName']:
                        gemeinsam.append(e["displayName"]+"("+str(round(float(e["degree"])*100, 2))+")")
                    break
                else:
                    continue
                break
            string =''
            gemeinsam = [x["displayName"]+"("+str(round(float(x["degree"])*100, 2))+")" for x in expert+student if (any(e['displayName'])==x['displayName'] for e in  expert) and (any(s['displayName'])==x['displayName'] for s in student)]
            if len(gemeinsam) == 1:
                string+= gemeinsam[0]
            elif len(gemeinsam)>1:
                string = gemeinsam[0]
                for index in range(1, len(gemeinsam)-1): 
                    string +=', '+ gemeinsam[index]

            return string

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

        if elem.text == "-gemeinsam-":
            expert = data[data['subject']+str(data['questionNumber'])+'_expert_keyword']
            student = data[data['subject']+str(data['questionNumber'])+'_keyword']
            sorted_expert = reversed(sorted(expert, key = lambda k:k['degree']))
            sorted_student = reversed(sorted(student, key = lambda k:k['degree']))
            
            string =''
            list_of_all_values = [value for elem in sorted_student
                      for value in elem.values()]
            gemeinsam = [x["displayName"] for x in sorted_expert if x['displayName'] in list_of_all_values]
            if len(gemeinsam) == 1:
                string+= gemeinsam[0]
            elif len(gemeinsam)>1:
                string = gemeinsam[0]
                for index in range(1, len(gemeinsam)-1): 
                    string +=', '+ gemeinsam[index]
            elem.text = string
            return elem

        if elem.text == "-unterschied1-":
            expert = data[data['subject']+str(data['questionNumber'])+'_expert_keyword']
            student = data[data['subject']+str(data['questionNumber'])+'_keyword']
            sorted_expert = reversed(sorted(expert, key = lambda k:k['degree']))
            sorted_student = reversed(sorted(student, key = lambda k:k['degree']))
            
            string =''
            list_of_all_values = [value for elem in sorted_student
                      for value in elem.values()]
            gemeinsam = [x["displayName"] for x in sorted_expert if x['displayName'] not in list_of_all_values]
            if len(gemeinsam) == 1:
                string+= gemeinsam[0]
            elif len(gemeinsam)>1:
                string = gemeinsam[0]
                for index in range(1, len(gemeinsam)-1): 
                    string +=', '+ gemeinsam[index]
            elem.text = string
            return elem

        if elem.text == "-unterschied2-":
            expert = data[data['subject']+str(data['questionNumber'])+'_expert_keyword']
            student = data[data['subject']+str(data['questionNumber'])+'_keyword']
            sorted_expert = reversed(sorted(expert, key = lambda k:k['degree']))
            sorted_student = reversed(sorted(student, key = lambda k:k['degree']))
            
            string =''
            list_of_all_values = [value for elem in sorted_expert
                      for value in elem.values()]
            gemeinsam = [x["displayName"] for x in sorted_student if x['displayName'] not in list_of_all_values]
            if len(gemeinsam) == 1:
                string+= gemeinsam[0]
            elif len(gemeinsam)>1:
                string = gemeinsam[0]
                for index in range(1, len(gemeinsam)-1): 
                    string +=', '+ gemeinsam[index]
            elem.text = string
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