from typing import Dict, List

from rb.cna.cna_graph import CnaGraph
from rb.cna.edge_type import EdgeType
from rb.core.document import Document
from rb.core.block import Block
from rb.core.lang import Lang
from rb.core.text_element import TextElement
from rb.similarity.vector_model import VectorModelType
from rb.similarity.vector_model_factory import create_vector_model
from rb.similarity.word2vec import Word2Vec
from rb.core.text_element_type import TextElementType
import matplotlib.pyplot as plt
import networkx as nx
import sys
import json
import pandas as pd
import numpy as np
import seaborn as sns
import networkx as nx
import logging
import os
import rb_api.keywords.keywords as keywords
from rb.processings.keywords.keywords_extractor import KeywordExtractor


def encode_element(element: TextElement, names: Dict[TextElement, str], graph: CnaGraph,  lang: Lang):
    keywords = KeywordExtractor.extract_keywords(False, text=element.text, lang=lang)
    count = len(keywords)
    keywords.sort(key=lambda x:x[1])	
    sorted_keywords = reversed(keywords)
    string =''
    if len(keywords) == 1:
        string+= keywords[0][1]
    elif len(keywords)>1:
        string = keywords[0][1]
        for index in range(1, len(keywords)-1): 
            string +=', '+ keywords[index][1]
    result =  { "name": names[element], "value": string, "type": element.depth, "importance": graph.importance[element] }
    if not element.is_sentence():
        result["children"] = [encode_element(child, names, graph, lang) for child in element.components]
    return result

def mergeelement( element):
    elementlist =[]
    if not (element.is_sentence() or element.is_word()):
        elementlist.append(element)
    for child in element.components:
        elementlist = elementlist + mergeelement(child)
    return elementlist

def compute_nxGraph(dataName, JsonName, docs, names, graph, edges, lang):
    log = logging.getLogger("my-logger")
    #LEXICAL_OVERLAP: CONTENT_OVERLAP
    G1 = nx.Graph()
    edge_labels1={}
    value1= []
    node_size1 = []

    #LEXICAL_OVERLAP: TOPIC_OVERLAP
    G2 = nx.Graph()
    edge_labels2={}
    value2= []
    node_size2 = []

    #LEXICAL_OVERLAP: ARGUMENT_OVERLAP
    G3 = nx.Graph()
    edge_labels3={}
    value3= []
    node_size3 = []

    #Graph for Word2vec
    G4 = nx.Graph()
    edge_labels4={}
    value4= []
    node_size4 = []


    color_map1 = []
    color_map2 = []
    color_map3 = []
    color_map4 = []

    textElement=[]
    for element in docs:
        if not element.is_sentence():
            elementlist = mergeelement(element)
            for index in elementlist:
                if not index.is_document():
                    if not G1.has_node(names[index].replace("Paragraph", "Absatz")): 
                        if (names[index].startswith('Paragraph 1')):
                            color_map1.append('#A0CBE2')
                        elif (names[index].startswith('Paragraph 2')):
                            color_map1.append('green')          
                        G1.add_node(names[index].replace("Paragraph", "Absatz"))
                        node_size1.append(int(graph.importance[index]*1000))
                        log.info(names[index])
                        
                        

                    if not G2.has_node(names[index]):  
                        G2.add_node(names[index].replace("Paragraph", "Absatz"))
                        node_size2.append(int(graph.importance[index]*1000))
                        if (names[index].startswith('Paragraph 1')):
                            color_map2.append('#fc0303')
                        if (names[index].startswith('Paragraph 2')):
                            color_map2.append('green')

                    if not G3.has_node(names[index]):  
                        G3.add_node(names[index].replace("Paragraph", "Absatz"))
                        node_size3.append(int(graph.importance[index]*1000))
                        if (names[index].startswith('Paragraph 1')):
                            color_map3.append('#fc0303')
                        if (names[index].startswith('Paragraph 2')):
                            color_map3.append('green')

                    if not G4.has_node(names[index]):  
                        G4.add_node(names[index].replace("Paragraph", "Absatz"))
                        node_size4.append(int(graph.importance[index]*1000))
                        if (names[index].startswith('Paragraph 1')):
                            color_map4.append('#fc0303')
                        if (names[index].startswith('Paragraph 2')):
                            color_map4.append('green')

                    keywords = KeywordExtractor.extract_keywords(False, text=index.text, lang=lang, threshold=0.0)
                    count = len(keywords)
                    keywords.sort(key=lambda x:x[1])	
                    sorted_keywords = reversed(keywords)
                    string =''
                    if len(keywords) == 1:
                        string+= keywords[0][1]
                    elif len(keywords)>1:
                        string = keywords[0][1]
                        for index2 in range(1, len(keywords)-1): 
                            string +=', '+ keywords[index2][1]


                    textElement.append((names[index], string))
                
                
    #X = []
    #Y = []
    #Z = []        
    for edge in edges:
        label =""
        if( not (edge['source'].startswith('Sentence') or edge['target'].startswith('Sentence') or edge['source'].startswith('Document') or edge['target'].startswith('Document'))):
            
            for type in edge['types']:           
                if type['name']=='LEXICAL_OVERLAP: CONTENT_OVERLAP' and float(type['weight'])>0:
                    if not G1.has_edge(edge['source'].replace("Paragraph", "Absatz"), edge['target'].replace("Paragraph", "Absatz")):
                        G1.add_edge(edge['source'].replace("Paragraph", "Absatz"), edge['target'].replace("Paragraph", "Absatz"))
                        value1.append((float(type['weight'])+0.6)*500)
                        log.info((float(type['weight'])+0.6)*500)
                        log.info(edge['source']+edge['target'])
                        #if (edge['source'].startswith('Paragraph 1') and edge['target'].startswith('Paragraph 2')):
                            #X.append(edge['source'].replace("Paragraph", "Absatz"))
                            #Y.append(edge['target'].replace("Paragraph", "Absatz"))
                            #Z.append((float(type['weight'])))
                        #edge_labels[(edge['source'], edge['target'])]= label
                if type['name']=='LEXICAL_OVERLAP: TOPIC_OVERLAP' and float(type['weight'])>0:
                    if not G2.has_edge(edge['source'], edge['target']):
                        G2.add_edge(edge['source'], edge['target'])
                        value2.append(int(float(type['weight'])*10))
                if type['name']=='LEXICAL_OVERLAP: ARGUMENT_OVERLAP' and float(type['weight'])>0:
                    if not G3.has_edge(edge['source'], edge['target']):
                        G3.add_edge(edge['source'], edge['target'])
                        value3.append(int(float(type['weight'])*10))
                if type['name']=='SEMANTIC: WORD2VEC(wiki)' and float(type['weight'])>0:
                    if not G4.has_edge(edge['source'], edge['target']):
                        G4.add_edge(edge['source'], edge['target'])
                        value4.append(int(float(type['weight'])*10))
            #if not G1.has_edge(edge['source'], edge['target']):
                #G1.add_edge(edge['source'], edge['target'])
                #value1.append(int(max(sim, 0)*100))
                #edge_labels[(edge['source'], edge['target'])]= label
    log.info(len(node_size3))
    log.info(G3.number_of_nodes())
    log.info(G1.number_of_edges())
    pos1 = nx.spring_layout(G1, k=2)
    options1 = {
    "node_color": color_map1,
    "edge_color": value1,
    "width": 2,
    "edge_cmap": plt.cm.Blues,
    "with_labels": True,
    "node_size":node_size1 
    }
    pos2 = nx.spring_layout(G2, k=2)
    options2 = {
    "node_color": "#03fc39",
    "edge_color": value2,
    "width": 2,
    "edge_cmap": plt.cm.Blues,
    "with_labels": True,
    "node_size":node_size2 
    }
    pos3 = nx.spring_layout(G3, k=2)
    options3 = {
    "node_color": "#fcbe03",
    "edge_color": value3,
    "width": 2,
    "edge_cmap": plt.cm.Blues,
    "with_labels": True,
    "node_size":node_size3
    }
    pos4 = nx.spring_layout(G4, k=2)
    options4 = {
    "node_color": "#A0CBE2",
    "edge_color": value4,
    "width": 2,
    "edge_cmap": plt.cm.Blues,
    "with_labels": True,
    "node_size":node_size4
    }
    plt.figure(figsize=(8, 9))
    nx.draw(G1, pos1, **options1)
    plt.savefig('rb_api/pandoc_filters/images/'+dataName+'_content.png', dpi=300)
    plt.clf()
    #data = pd.DataFrame(data={'x':X, 'y':Y, 'z':Z})
    #data = data.pivot(index='x', columns='y', values='z')
    #sns.heatmap(data)
    #plt.savefig('rb_api/pandoc_filters/images/'+dataName+'_content_heat.png', dpi=300)
    #plt.clf()
    #plt.figure(figsize=(8, 7))
    #nx.draw(G2, pos2, **options2)
    #plt.savefig('rb_api/pandoc_filters/images/'+dataName+'_topic.png', dpi=300)
    #plt.clf()
    #plt.figure(figsize=(8, 7))
    #nx.draw(G3, pos3, **options3)
    #plt.savefig('rb_api/pandoc_filters/images/'+dataName+'_argument.png', dpi=300)
    #plt.clf()
    #plt.figure(figsize=(8, 7))  
    #nx.draw(G4, pos4, **options4)
    #plt.savefig('rb_api/pandoc_filters/images/'+dataName+'_word2vec.png', dpi=300)
    #plt.clf()
    data = getJson('rb_api/pandoc_filters/'+JsonName+'.json')
    data.update({dataName: textElement})
    with open('rb_api/pandoc_filters/'+JsonName+'.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True


def getJson(url):
    varData= {}
    if os.path.isfile(url):
        # checks if file exists
        print ("File exists ")
        with open(url, encoding='UTF-8') as f:
            varData = json.load(f)
    return varData

def compute_graph(dataName, JsonName, texts: List[str], lang: Lang, models: List) -> str:
    docs = [Document(lang=lang, text=text) for text in texts]
    models = [create_vector_model(lang, VectorModelType.from_str(model["model"]), model["corpus"]) for model in models]
    models = [model for model in models if model is not None]
    graph = CnaGraph(docs=docs, models=models)
    sentence_index = 1
    doc_index = 1
    names = {}
    for doc_index, doc in enumerate(docs):
        names[doc] = "Document {}".format(doc_index+1)
        for paragraph_index, paragraph in enumerate(doc.components):
            names[paragraph] = "Paragraph {}.{}".format(doc_index+1, paragraph_index+1)
            for sentence_index, sentence in enumerate(paragraph.components):
                names[sentence] = "Sentence {}.{}.{}".format(doc_index + 1, paragraph_index + 1, sentence_index + 1)
    result = {"data": {
        "name": "Document Set", "value": None, "type": None, "importance": None,
        "children": [encode_element(doc, names, graph, lang) for doc in docs]}
        }
    edges = {}
    for a, b, data in graph.graph.edges(data=True):
        if data["type"] is not EdgeType.ADJACENT and data["type"] is not EdgeType.PART_OF:
            if data["type"] is EdgeType.COREF:
                edge_type = EdgeType.COREF.name
            else:
                edge_type = "{}: {}".format(data["type"].name, data["model"].name)
            if (names[a], names[b]) not in edges:
                edges[(names[a], names[b])] = []
            edge = {
                "name": edge_type,
                "weight": str(data["value"]) if "value" in data else None,
                "details": data["details"] if "details" in data else None,
            }
            edges[(names[a], names[b])].append(edge)
    edges = [
        {
            "source": pair[0],
            "target": pair[1],
            "types": types,
        }
        for pair, types in edges.items()
    ]
    compute_nxGraph(dataName, JsonName, docs, names, graph, edges, lang)
    result["data"]["edges"] = edges
    return result

def compute_graph_cscl(texts: List[str], lang: Lang, models: List, textLabels: List[str]) -> str:
    blocks = [Block(lang=lang, text=text) for text in texts]
    models = [create_vector_model(lang, VectorModelType.from_str(model["model"]), model["corpus"]) for model in models]
    models = [model for model in models if model is not None]
    graph = CnaGraph(docs=blocks, models=models)
    sentence_index = 1
    block_index = 1
    names = {}
    for block_index, block in enumerate(blocks):
        names[block] = "{} {}".format(textLabels[0], block_index+1)
        for paragraph_index, paragraph in enumerate(block.components):
            names[paragraph] = "{} {}.{}".format(textLabels[1], block_index+1, paragraph_index+1)
    result = {"data": {
        "name": "Document Set", "value": None, "type": None, "importance": None,
        "children": [encode_element(block, names, graph, lang) for block in blocks]}
        }
    edges = {}
    for a, b, data in graph.graph.edges(data=True):
        if data["type"] is not EdgeType.ADJACENT and data["type"] is not EdgeType.PART_OF:
            if data["type"] is EdgeType.COREF:
                edge_type = EdgeType.COREF.name
            else:
                edge_type = "{}: {}".format(data["type"].name, data["model"].name)
            if (names[a], names[b]) not in edges:
                edges[(names[a], names[b])] = []
            edge = {
                "name": edge_type,
                "weight": str(data["value"]) if "value" in data else None,
                "details": data["details"] if "details" in data else None,
            }
            edges[(names[a], names[b])].append(edge)
    edges = [
        {
            "source": pair[0],
            "target": pair[1],
            "types": types,
        }
        for pair, types in edges.items()
    ]
    result["data"]["edges"] = edges
    return result
