# -*- coding: utf-8 -*-
"""
Created on Fri Apr 11 15:54:03 2025

@author: dell
"""
import argparse
import json
from utils import Decoder
import time

def parse_arguments():
    parser = argparse.ArgumentParser(description="Abstract") 
    parser.add_argument("--model", type=str, default='doubao', choices=["doubao", "chatglm", "gemini", "deepseek"])
    parser.add_argument("--random_seed", type=int, default=1, help="random seed")
    parser.add_argument(
        "--method", type=str, default="zero_shot", choices=["zero_shot", "zero_shot_cot", "few_shot", "few_shot_cot"], help="method"
    )
    parser.add_argument(
        "--max_length", type=int, default=512, help="maximum length of output tokens by model for reasoning extraction"
    )
    parser.add_argument(
        "--api_time_interval", type=float, default=0.1, help=""
    )
    args = parser.parse_args()    
    return args

def cleanObject( pred ):
    
    object = eval( pred )
    return object

def genObject( decoder, args, source, prompt ):
    prompt = prompt.format( source )
    for _ in range( 3 ):
        try:
            pred = decoder.decode(args, prompt, args.max_length)
            object = cleanObject(pred)
            return object
        except:
            pass
    return {'Object': ''}

def saveJson( objectFile, objects ):
    # 将数据保存为JSON文件
    with open(objectFile, "w", encoding="utf-8") as f:
        json.dump(objects, f, indent=4, ensure_ascii=False)


def readPrompt( promptFile ):
    with open(promptFile, 'rt', encoding='utf-8') as f:
        prompt = f.read()
    assert( '{}' in prompt) 
    return prompt

def extractContext():
    args = parse_arguments()
    decoder = Decoder(args)
    dataset = "acl"
    promptFile = f"D:/NLPWorkspace/abstract/dataset/{dataset}/prompts/提取主题/主题提取提示词.txt"
    inputFile = f"D:/NLPWorkspace/abstract/dataset/{dataset}/gold-split/context.json"
    objectFile = f"D:/NLPWorkspace/abstract/dataset/{dataset}/doubao/objectShuffled/doubao-object-shuffled.json"
    objects = []
    with open(inputFile, 'r', encoding='utf-8') as f:
        data = json.load(f)   
    prompt = readPrompt( promptFile )
    for item in data:
        source = item['Context']
        obj = genObject(decoder, args, source, prompt )
        obj['Context'] = source
        objects.append( obj )
        try:
            time.sleep( 20 )
        except:
            pass
    saveJson( objectFile, objects )

def extractAbstract():
    args = parse_arguments()
    decoder = Decoder(args)
    dataset = "acl"
    promptFile = f"D:/NLPWorkspace/abstract/dataset/{dataset}/prompts/从摘要提取主题/主题提取提示词.txt"
    inputFile = f"D:/NLPWorkspace/abstract/dataset/{dataset}/gold-split/abstract-300.json"
    objectFile = f"D:/NLPWorkspace/abstract/dataset/{dataset}/doubao/objectfromabstract/doubao-object-abstract.json"
    objects = []
    with open(inputFile, 'r', encoding='utf-8') as f:
        data = json.load(f)   
    prompt = readPrompt( promptFile )
    for item in data:
        source = item['abstract']
        obj = genObject(decoder, args, source, prompt )
        obj['abstract'] = source
        objects.append( obj )
        try:
            time.sleep( 20 )
        except:
            pass
    saveJson( objectFile, objects )
    
if __name__ == '__main__':
      extractAbstract() 
        
        
        
        
        
        