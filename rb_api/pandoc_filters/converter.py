import pypandoc
import os
import json
from PyPDF2 import PdfFileMerger, PdfFileReader
import sys

def getJson(url):
    with open(url, encoding='UTF-8') as f:
        varData = json.load(f)
    return varData

def convert_file(topicName, topicSize):
    """data ={
    'subject' : 'Übungsname',
    'question' : 'questionnumber',
    'keyword' : 8.6,
    'cna' : '9976770500',
    'figure':'wordnet'
    }"""
    
    """
    os.system("chmod +x rb_api/pandoc_filters/caps.py")
    os.system("chmod +x rb_api/pandoc_filters/keywordVIz.py")
    os.system("chmod +x rb_api/pandoc_filters/Viz.py")
    os.system("pyinstaller --onefile rb_api/pandoc_filters/Viz.py")
    
    stream = os.popen(' cat rb_api/pandoc_filters/template_main.md | pandoc -s -f gfm -t json | python3 rb_api/pandoc_filters/keywordVIz.py  | pandoc -s -f json -o rb_api/output/pdf/'+data['subject']+data['question']+'somefile.pdf')
    output = stream.read()
    print(output)
    """

    
    
    fileURL='rb_api/pandoc_filters/'+topicName+'.pdf'
    
    os.system("chmod +x rb_api/pandoc_filters/subjectName.py")
    os.system("chmod +x rb_api/pandoc_filters/keywordVIz.py")
    #filters = ['rb_api/pandoc_filters/caps.py']
    #pdoc_args = ['--mathjax', '--smart']
    #output = pypandoc.convert_file('rb_api/pandoc_filters/template_main.md', 'pdf' , filters=filters, outputfile=fileURL)
    if topicSize == 1:
        data = getJson('rb_api/pandoc_filters/'+topicName+'.json')
        data.update({'subject': topicName})
        data.update({'questionNumber': topicSize})
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        stream = os.popen('pandoc -V geometry:paperwidth=4in -V geometry:paperheight=6in -V geometry:margin=.5in rb_api/pandoc_filters/template_main.md  --pdf-engine=xelatex -o rb_api/pandoc_filters/'+topicName+'.pdf --filter rb_api/pandoc_filters/subjectName.py --resource-path=rb_api/pandoc_filters/')
        output = stream.read()
        print(output)
        fileURL='rb_api/pandoc_filters/'+topicName+'.pdf'
        return fileURL
    if topicSize > 1:
        data = getJson('rb_api/pandoc_filters/'+topicName+'.json')
        data.update({'subject': topicName})
        data.update({'questionNumber': 1})
        
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        stream = os.popen('pandoc -V geometry:paperwidth=4in -V geometry:paperheight=6in -V geometry:margin=.5in rb_api/pandoc_filters/template_main.md  --pdf-engine=xelatex -o rb_api/pandoc_filters/'+topicName+'_1.pdf --filter rb_api/pandoc_filters/subjectName.py --resource-path=rb_api/pandoc_filters/')
        output = stream.read()
        print(output)
        for fileNumber in range(2, topicSize+1):
            data = getJson('rb_api/pandoc_filters/'+topicName+'.json')
            data.update({'subject': topicName})
            data.update({'questionNumber': fileNumber})
            
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            stream = os.popen('pandoc -V geometry:paperwidth=4in -V geometry:paperheight=6in -V geometry:margin=.5in rb_api/pandoc_filters/template_main.md  --pdf-engine=xelatex -o rb_api/pandoc_filters/'+topicName+'_'+str(fileNumber)+'.pdf --filter rb_api/pandoc_filters/subjectName.py --resource-path=rb_api/pandoc_filters/')
            output = stream.read()
            print(output)
    #print(output)

    #stream = os.popen(' cat rb_api/pandoc_filters/template.md | pandoc -s -f gfm -t json | python3 rb_api/pandoc_filters/keywordVIz.py  | pandoc -s -f json -o rb_api/pandoc_filters/template1.md')
    #output = stream.read()
    #print(output)

    #stream = os.popen('pandoc -i rb_api/pandoc_filters/template1.md --filter pandoc-run-filter  -o rb_api/output/pdf/'+data['subject']+data['question']+'somefile.pdf')
    #output = stream.read()
    #print(output)
            
            pdf_cat(topicName, topicSize, fileURL)
    return fileURL

def pdf_cat(topicName, topicSize, outputName):
    # Call the PdfFileMerger
    mergedObject = PdfFileMerger()
    
    # I had 116 files in the folder that had to be merged into a single document
    # Loop through all of them and append their pages
    for fileNumber in range(1, topicSize+1):
        mergedObject.append(PdfFileReader('rb_api/pandoc_filters/'+topicName + '_' + str(fileNumber)+ '.pdf', 'rb'))
    
    # Write all the files into a file which is named as shown below
    mergedObject.write(outputName)


    