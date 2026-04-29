# -*- coding: utf-8 -*-
"""
Created on Thu Apr  9 09:46:27 2026

@author: dell
"""

import requests
import json
import time
from tqdm import tqdm

myyear= 2025

OUTPUT_JSON = f"D:/NLPWorkspace/abstract/dataset/mcp/year2020-2025/mcp{myyear}.json"

# EAAI 在 OpenAlex 的 source ID（固定）
SOURCE_ID = "S4210189124" #"S140653181" #"S123456789"  # ⚠️ 我们下面会自动获取真实ID

BASE_URL = "https://api.openalex.org/works"


def get_source_id():
    """获取期刊在 OpenAlex 的 source_id"""
    url = "https://api.openalex.org/sources"
    params = {
        "filter": 'display_name.search:"Molecular and Cellular Proteomics"'
    }
    r = requests.get(url, params=params)
    data = r.json()

    for item in data["results"]:
        if item["display_name"] == "Molecular and Cellular Proteomics":
            return item["id"].split("/")[-1]

    return None

def get_source_id_by_issn(issn):
    url = "https://api.openalex.org/sources"
    params = {
        "filter": f"issn:{issn}"
    }

    r = requests.get(url, params=params)
    data = r.json()

    if data["results"]:
        return data["results"][0]["id"].split("/")[-1]

    return None




def reconstruct_abstract(inv_index):
    """将 inverted_index 还原成文本"""
    if not inv_index:
        return None

    word_positions = {}
    for word, positions in inv_index.items():
        for pos in positions:
            word_positions[pos] = word

    return " ".join(word_positions[i] for i in sorted(word_positions))


def get_all_papers(source_id):
    """获取2025年所有论文"""
    results = []
    cursor = "*"

    print("🔍 正在抓取论文...")

    while True:
        params = {
            "filter": f"primary_location.source.id:{source_id},publication_year:{myyear}",
            "per-page": 200,
            "cursor": cursor
        }

        r = requests.get(BASE_URL, params=params)
        data = r.json()

        works = data.get("results", [])
        if not works:
            break

        for w in works:
            abstract = reconstruct_abstract(w.get("abstract_inverted_index"))

            results.append({
                "id": w.get("id"),
                "title": w.get("title"),
                "abstract": abstract,
                "doi": w.get("doi"),
                "publication_date": w.get("publication_date")
            })

        print(f"已获取 {len(results)} 篇论文")

        cursor = data["meta"].get("next_cursor")
        if not cursor:
            break

        time.sleep(0.5)

    return results


def main():
    print("📚 获取期刊ID...")
    #source_id = get_source_id()
    source_id = get_source_id_by_issn("1535-9476")

    if not source_id:
        print("❌ 未找到期刊")
        return

    print(f"✅ 期刊ID: {source_id}")

    papers = get_all_papers(source_id)

    print(f"\n💾 保存 {len(papers)} 篇论文到文件")

    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(papers, f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    main()