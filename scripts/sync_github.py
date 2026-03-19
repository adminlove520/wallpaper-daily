#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import json
import urllib.request
from datetime import datetime

REPO = "IT-NuanxinPro/nuanXinProPic"

def get_latest_from_metadata(category):
    """从 metadata JSON 获取最新图片"""
    try:
        if category == "desktop":
            meta_file = "desktop.json"
        elif category == "mobile":
            meta_file = "mobile.json"
        elif category == "avatar":
            meta_file = "avatar.json"
        else:
            return None
        
        meta_url = "https://cdn.jsdelivr.net/gh/%s@latest/metadata/%s" % (REPO, meta_file)
        req = urllib.request.Request(meta_url)
        resp = urllib.request.urlopen(req, timeout=30)
        data = json.loads(resp.read().decode('utf-8'))
        
        images = data.get("images", {})
        if not images:
            return None
        
        sorted_images = sorted(
            images.items(),
            key=lambda x: x[1].get("createdAt", ""),
            reverse=True
        )
        
        first_path, info = sorted_images[0]
        
        url = "https://cdn.jsdelivr.net/gh/%s@latest/%s" % (REPO, first_path)
        
        # title 优先用 ai.displayTitle
        ai_info = info.get("ai", {})
        title = ai_info.get("displayTitle") or info.get("filename", "")
        if title and "." in title:
            title = title.rsplit(".", 1)[0]
        
        return {"title": title, "url": url}
        
    except Exception as e:
        print("Error in %s: %s" % (category, e), flush=True)
        return None

def main():
    print("同步壁纸数据...", flush=True)
    
    categories = {}
    
    # Bing
    try:
        req = urllib.request.Request("https://wallpaper.061129.xyz/data/bing/latest.json")
        req.add_header("User-Agent", "wallpaper-sync-bot")
        bing = json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))
        item = bing.get("items", [None])[0]
        if item:
            urlbase = item.get("urlbase", "")
            categories["bing"] = {
                "title": item.get("title", ""),
                "url": "https://www.bing.com%s_1920x1080.jpg" % urlbase
            }
        else:
            categories["bing"] = None
    except Exception as e:
        print("Bing error: %s" % e, flush=True)
        categories["bing"] = None
    
    categories["desktop"] = get_latest_from_metadata("desktop")
    categories["mobile"] = get_latest_from_metadata("mobile")
    categories["avatar"] = get_latest_from_metadata("avatar")
    
    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "generatedAt": datetime.now().isoformat() + "Z",
        "categories": categories
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2), flush=True)
    
    out_path = os.path.join(os.path.dirname(__file__), "..", "api", "today.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("已写入: %s" % out_path, flush=True)

if __name__ == "__main__":
    main()
