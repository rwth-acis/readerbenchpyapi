import pypandoc
import os
import json

def convert_file():
    data ={
    'subject' : 'Übungsname',
    'question' : 'questionnumber',
    'keyword' : 8.6,
    'cna' : '9976770500',
    'figure':'wordnet'
    }
    fileURL="rb_api/output/pdf/"+data['subject']+data['question']+"somefile.pdf"
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    """
    os.system("chmod +x rb_api/pandoc_filters/caps.py")
    os.system("chmod +x rb_api/pandoc_filters/keywordVIz.py")
    os.system("chmod +x rb_api/pandoc_filters/Viz.py")
    os.system("pyinstaller --onefile rb_api/pandoc_filters/Viz.py")
    
    stream = os.popen(' cat rb_api/pandoc_filters/template.md | pandoc -s -f gfm -t json | python3 rb_api/pandoc_filters/keywordVIz.py  | pandoc -s -f json -o rb_api/output/pdf/'+data['subject']+data['question']+'somefile.pdf')
    output = stream.read()
    print(output)
    """

    
    
    
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    os.system("chmod +x rb_api/pandoc_filters/subjectName.py")
    os.system("chmod +x rb_api/pandoc_filters/keywordVIz.py")
    #filters = ['rb_api/pandoc_filters/caps.py']
    #pdoc_args = ['--mathjax', '--smart']
    #output = pypandoc.convert_file('rb_api/pandoc_filters/template.md', 'pdf' , filters=filters, outputfile=fileURL)
    stream = os.popen('pandoc rb_api/pandoc_filters/template.md  --pdf-engine=xelatex -o rb_api/output/pdf/'+data['subject']+data['question']+'somefile.pdf --filter rb_api/pandoc_filters/subjectName.py --resource-path=rb_api/pandoc_filters/')
    output = stream.read()
    print(output)
    #print(output)

    #stream = os.popen(' cat rb_api/pandoc_filters/template.md | pandoc -s -f gfm -t json | python3 rb_api/pandoc_filters/keywordVIz.py  | pandoc -s -f json -o rb_api/pandoc_filters/template1.md')
    #output = stream.read()
    #print(output)

    #stream = os.popen('pandoc -i rb_api/pandoc_filters/template1.md --filter pandoc-run-filter  -o rb_api/output/pdf/'+data['subject']+data['question']+'somefile.pdf')
    #output = stream.read()
    #print(output)
    return fileURL

    