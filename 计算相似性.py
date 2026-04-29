# -*- coding: utf-8 -*-
"""
Created on Thu Apr 23 15:03:01 2026

@author: dell
"""
import json

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
model = SentenceTransformer('all-MiniLM-L6-v2')
print("Loaded successfully")

gold = "D:/NLPWorkspace/abstract/dataset/mcp/gold-object/gold-prompts0.json"
contextobject = "D:/NLPWorkspace/abstract/dataset/mcp/doubao/object/doubao-results0.json"
abstratobject = "D:/NLPWorkspace/abstract/dataset/mcp/doubao/objectfromabstract/doubao-results0.json"

with open(gold, "r", encoding="utf-8") as f:
    golddata = json.load(f)
with open(contextobject, "r", encoding="utf-8") as f:
    contextdata = json.load(f)
with open(abstratobject, "r", encoding="utf-8") as f:
    abstratdata = json.load(f)

contextsim = []
assert( len(golddata) == len(contextdata) )
for go, co in zip(golddata, contextdata):
    emb1 = model.encode([go['Object']])
    emb2 = model.encode([co['Object']])
    sim = cosine_similarity(emb1, emb2)[0][0]
    contextsim.append( sim )
    
abstractsim = []
for i in range(len(abstratdata)):
    go, ao = golddata[i], abstratdata[i]
    emb1 = model.encode([go['Object']])
    emb2 = model.encode([ao['Object']])
    sim = cosine_similarity(emb1, emb2)[0][0]
    abstractsim.append( sim )

print( round(sum(contextsim)/len(contextsim),2), round(sum(abstractsim)/len(abstractsim),2))    