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


def encode_element(element: TextElement, names: Dict[TextElement, str], graph: CnaGraph):
    result =  { "name": names[element], "value": element.text, "type": element.depth, "importance": graph.importance[element] }
    if not element.is_sentence():
        result["children"] = [encode_element(child, names, graph) for child in element.components]
    return result

def compute_nxGraph(dataName, JsonName, docs, names, graph, edges):
    G = nx.Graph()
    edge_labels={}
    for element in docs:
        if not element.is_sentence():
            G.add_node(names[element],weight=graph.importance[element])
    for edge in edges:
        label =""
        for type in edge['types']:
            if type['name']=='LEXICAL_OVERLAP: CONTENT_OVERLAP':
                label+= "A:"+ round(type['weight'], 2)
            if type['name']=='LEXICAL_OVERLAP: TOPIC_OVERLAP':
                label+= "B:"+ round(type['weight'], 2)
            if type['name']=='LEXICAL_OVERLAP: ARGUMENT_OVERLAP':
                label+= "C:"+ round(type['weight'], 2)
            if type['name']=='SEMANTIC: WORD2VEC(wiki)':
                label+= "D:"+ round(type['weight'], 2)
        G.add_edge(edge['source'], edge['target'])
        edge_labels[(edge['source'], edge['target'])]= label
    pos = nx.nx_agraph.graphviz_layout(G, prog="twopi")
    
    nx.draw(G, with_labels = True, node_size=1500, node_color="skyblue", pos=pos)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    plt.savefig('rb_api/pandoc_filters/images/'+dataName+'.png')

    data = getJson('rb_api/pandoc_filters/'+JsonName+'.json')
    data.update({'cnaUrl': 'rb_api/pandoc_filters/images/'+dataName+'.png'})
    with open('rb_api/pandoc_filters'+JsonName+'.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    return True

def getJson(url):
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
        "children": [encode_element(doc, names, graph) for doc in docs]}
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
    compute_nxGraph(dataName, JsonName, docs, names, graph, edges)
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
        "children": [encode_element(block, names, graph) for block in blocks]}
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
