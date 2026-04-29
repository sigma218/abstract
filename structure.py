# -*- coding: utf-8 -*-
"""
Created on Sun Apr 26 09:03:16 2026

@author: dell
"""
import json
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer('all-MiniLM-L6-v2')

def similarity(text1, text2):    
    emb1 = model.encode([text1])
    emb2 = model.encode([text2])
    sim = cosine_similarity(emb1, emb2)[0][0]
    return sim

def segmentation( golddata, doubaodata ):
    score = {'Context':0, 'Method':0, 'Result':0, 'Contribution':0, 'Other':0}
    number = {'Context':0, 'Method':0, 'Result':0, 'Contribution':0, 'Other':0}
    for g, p in zip(golddata, doubaodata):
        for key in g['Decomposition'].keys():
            if key in p['components'].keys():
                assert( key in score.keys() and key in number.keys() )
                goldString = g['Decomposition'][key]
                doubaoString = p['components'][key]
                sim = similarity(goldString, doubaoString)
                score[key] += sim
                number[key] += 1
    for key in score.keys():
        if number[key] > 0:
            print( round(score[key] / number[key], 3))

def object( golddata, doubaodata ):
    simila = 0
    for g, p in zip(golddata, doubaodata):
        try:
            goldobject = g['Object']
        except:
            print( g['Context'][0:30] )
        try:
            doubaoobject = p['Object']
        except:
            print( p['Context'][0:30] )
        sim = similarity(goldobject, doubaoobject)
        simila += sim
    print( round(simila/len(golddata),3) )

def structure( golddata, doubaodata ):
    precision = 0
    recall = 0
    f1 = 0
    
    for g, p in zip(golddata, doubaodata):
        G = set(g['Decomposition'].keys())
        P = set(p['components'].keys())
        inter = G & P
        precision += len(inter) / len(P)
        recall += len(inter) / len(G)
        f1 += 2*precision*recall / (precision + recall)
        
    precision /= len(golddata)
    recall /= len(golddata)
    f1 /= len(golddata)
    
    print(round(precision,3), round(recall,3), round(f1,3))

if __name__ == "__main__":
    gold = "./finaldataset/mcp/gold/gold-object.json"
    doubao = "./finaldataset/mcp/doubao/doubao-object.json"
    with open(gold, "r", encoding="utf-8") as f:
        golddata = json.load(f)
        
    with open(doubao, "r", encoding="utf-8") as f:
        doubaodata = json.load(f)
        print( len(doubaodata) )
    assert( len(golddata) == len(doubaodata) )
    object( golddata, doubaodata )