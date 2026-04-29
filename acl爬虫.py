# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 14:30:28 2026

@author: dell
"""
import os
import json
import random


import re
import json
import os

def extract_papers_from_acl2025(html_file, output_file):
    """
    从ACL 2025 HTML文件中提取论文标题和摘要
    
    Args:
        html_file: 输入的HTML文件路径
        output_file: 输出的JSON文件路径
    """
    
    # 读取HTML文件
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 存储所有论文
    papers = []
    
    # 分割出各个论文块（每个论文在一个d-sm-flex align-items-stretch mb-3的div中）
    paper_blocks = re.split(r'<div class="d-sm-flex align-items-stretch mb-3">', content)[1:]
    
    print(f"找到 {len(paper_blocks)} 个潜在论文块")
    
    for block in paper_blocks:
        # 提取标题和链接
        title_match = re.search(
            r'<strong><a class="align-middle" href="([^"]*)">(.*?)</a></strong>', 
            block
        )
        if not title_match:
            continue
        
        href = title_match.group(1)
        title_html = title_match.group(2)
        
        # 清理标题中的HTML标签
        title = re.sub(r'<[^>]+>', '', title_html).strip()
        
        # 从href中提取论文ID
        # href格式: https://aclanthology.org/2025.acl-long.1/
        id_match = re.search(r'/((?:\d+\.)?[^/]+)/?$', href)
        if not id_match:
            continue
        
        paper_id = id_match.group(1)
        # 构造abstract的id (例如: 2025.acl-long.1 -> abstract-2025--acl-long--1)
        abstract_id = f'abstract-{paper_id.replace(".", "--")}'
        
        # 在整个文档中查找对应的摘要
        abstract_pattern = (
            f'<div class="card bg-light mb-2 mb-lg-3 collapse abstract-collapse" '
            f'id="{abstract_id}"><div class="card-body p-3 small">(.*?)</div></div>'
        )
        abstract_match = re.search(abstract_pattern, content, re.DOTALL)
        
        if abstract_match:
            abstract_html = abstract_match.group(1)
            # 清理摘要中的HTML标签
            abstract = re.sub(r'<[^>]+>', '', abstract_html).strip()
            
            if abstract:  # 只保存有摘要的论文
                papers.append({
                    'title': title,
                    'abstract': abstract
                })
    
    print(f"成功提取 {len(papers)} 篇论文（含摘要）")
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # 保存为JSON文件
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)
    
    print(f"已保存到 {output_file}")
    return papers

# 主程序
if __name__ == "__main__":
    year = 2020
    input_file = f"./dataset/ACL{year}.html"
    output_file = f"./dataset/acl{year}.json"
    
    papers = extract_papers_from_acl2025(input_file, output_file)
    
    # 显示前几篇作为示例
    print("\n前3篇论文示例:")
    for i, paper in enumerate(papers[:3]):
        print(f"\n--- 论文 {i+1} ---")
        print(f"标题: {paper['title'][:80]}...")
        print(f"摘要: {paper['abstract'][:100]}...")



