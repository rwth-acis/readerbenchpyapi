import json
from typing import Dict, List, Tuple

from flask import Flask, jsonify, request
from rb.complexity.complexity_index import compute_indices
from rb.complexity.index_category import IndexCategory
from rb.core.document import Document
from rb.core.lang import Lang
from rb.core.text_element import TextElement
from rb.core.word import Word
from rb.processings.keywords.keywords_extractor import KeywordExtractor
from rb.similarity.vector_model import (CorporaEnum, VectorModel,
                                        VectorModelType)
from rb.similarity.vector_model_factory import VECTOR_MODELS, get_default_model
from rb.utils.utils import str_to_lang

from nltk.corpus import wordnet as wn
import networkx as nx
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

app = Flask(__name__)


def keywordsOption():
    return ""

def transform_for_visualization(dataName, JsonName, textType, keywords: List[Tuple[int, Word]], lang: Lang) -> Dict:

    vector_model: VectorModel = get_default_model(lang)
    edge_list, node_list = [], []
    
    G = nx.Graph()
    edge_labels={}
    
    from_node = []
    to_node = []
    value= []

    for kw in keywords:
        node_list.append({
            "type": "Word",
            "uri": kw[1],
            "displayName": kw[1],
            "active": True,
            "degree": str(max(0, float(kw[0])))
        })
        #G.add_node(kw[1],weight=max(0, float(kw[0])))

    for i, kw1 in enumerate(keywords):
        for j, kw2 in enumerate(keywords):
            try:
                sim = vector_model.similarity(vector_model.get_vector(kw1[1]), vector_model.get_vector(kw2[1]))
                if i != j and sim >= 0.3:
                    edge_list.append({
                        "edgeType": "SemanticDistance",
                        "score": str(max(sim, 0)),
                        "sourceUri": kw1[1],
                        "targetUri": kw2[1]
                    })
                    print("Problem with ****************************************")
                    
                    from_node.append(kw1[1])
                    to_node.append(kw2[1])
                    value.append(int(max(sim, 0)*10))
                    
                    #G.add_edge(kw1[1], kw2[1], weight=max(sim, 0))
                    #G.add_edge(str(kw1[1]), str(kw2[1]))
                    #edge_labels[(str(kw1[1]), str(kw2[1]))]= round(max(sim, 0), 2)
            except:
                print("Problem with " + kw1[1] + " or " + kw2[1])

    
        
    #pos = nx.nx_agraph.graphviz_layout(G, prog="twopi")
    
    #nx.draw(G, with_labels = True, node_size=1500, node_color="skyblue", pos=pos)
    #nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    
    # Build a dataframe with your connections
    df = pd.DataFrame({ 'from':from_node, 'to':to_node, 'value':value})
    # Build your graph
    G=nx.from_pandas_edgelist(df, 'from', 'to', create_using=nx.Graph() )
    pos = nx.spring_layout(G, seed=63)
    options = {
    "node_color": "#A0CBE2",
    "edge_color": value,
    "width": 4,
    "edge_cmap": plt.cm.Blues,
    "with_labels": False,
    }
    nx.draw(G, pos, **options)
    # Custom the nodes:
    #nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_color=df['value'], width=10.0, edge_cmap=plt.cm.Blues)
    plt.savefig('rb_api/pandoc_filters/images/'+ dataName +'.png', dpi=199)
    plt.clf()
    data = getJson('rb_api/pandoc_filters/'+JsonName+'.json')
    data.update({textType : 'rb_api/pandoc_filters/images/'+dataName+'.png'})
    with open('rb_api/pandoc_filters'+JsonName+'.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return {
        "data": {
            "edgeList": edge_list,
            "nodeList": node_list
        },
        "success": True,
        "errorMsg": ""
    }

def getJson(url):
    varData= {}
    if os.path.isfile(url):
        # checks if file exists
        print ("File exists ")
        with open(url, encoding='UTF-8') as f:
            varData = json.load(f)
    return varData

def keywordsPost():
    """TODO, not working"""
    params = json.loads(request.get_data())
    posTagging = params.get('pos-tagging')
    bigrams = params.get('bigrams')
    text = params.get('text')
    languageString = params.get('language')
    lang = str_to_lang(languageString)
    threshold = params.get('threshold')
    plotName = "wordnet"
    #plotName = params.get('saveAs')

    # if lang is Lang.RO:
    #     vector_model = VECTOR_MODELS[lang][CorporaEnum.README][VectorModelType.WORD2VEC](
    #         name=CorporaEnum.README.value, lang=lang)
    # elif lang is Lang.EN:
    #     vector_model = VECTOR_MODELS[lang][CorporaEnum.COCA][VectorModelType.WORD2VEC](
    #         name=CorporaEnum.COCA.value, lang=lang)
    # elif lang is Lang.ES:
    #     vector_model = VECTOR_MODELS[lang][CorporaEnum.JOSE_ANTONIO][VectorModelType.WORD2VEC](
    #         name=CorporaEnum.JOSE_ANTONIO.value, lang=lang)

    # lsa = params.get('lsa')
    # lda = params.get('lda')
    # w2v = params.get('w2v')
    # threshold = params.get('threshold')

    # textElement = Document(lang=lang, text=text, vector_model=vector_model)
    # print(textElement.keywords)
    dataName =  params.get('saveAs') 
    textType = params.get('type')
    JsonName = params.get('topicName')
    keywords = KeywordExtractor.extract_keywords(text=text, lang=lang)
    return jsonify(transform_for_visualization(dataName, JsonName, textType, keywords=keywords, lang=lang))
