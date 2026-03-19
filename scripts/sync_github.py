#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import sys
import json
import urllib.request
from datetime import datetime

if sys.version_info[0] >= 3:
    import urllib.parse as urlparse
else:
    import urllib as urlparse

REPO = "IT-NuanxinPro/nuanXinProPic"

def gh_request_raw(path):
    """原始请求，不编码"""
    url = "https://api.github.com/repos/%s/%s" % (REPO, path)
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "wallpaper-sync-bot")
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode('utf-8'))

def gh_request(path):
    """带URL编码的请求"""
    # 对路径进行UTF-8编码后再URL编码
    if isinstance(path, str):
        path = path.encode('utf-8')
    encoded_path = urlparse.quote(path, safe='/')
    url = "https://api.github.com/repos/%s/%s" % (REPO, encoded_path)
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "wallpaper-sync-bot")
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode('utf-8'))

def get_latest(category):
    try:
        if category == "desktop":
            base = "preview/desktop"
        elif category == "mobile":
            base = "preview/mobile"
        elif category == "avatar":
            base = "wallpaper/avatar"
        else:
            return None
        
        # 获取目录列表 - 需要编码
        contents = gh_request(base)
        latest = None
        latest_date = ""
        
        for item in contents:
            if item.get("type") != "dir":
                continue
            # 获取子目录 - 需要编码
            sub = gh_request(item["path"])
            for f in sub:
                if f.get("type") != "file":
                    continue
                updated = f.get("updated_at", "")
                if updated > latest_date:
                    latest_date = updated
                    latest = f
        
        if latest:
            name = latest.get("name", "").rsplit(".", 1)[0]
            path = latest.get("path", "")
            # 对路径进行URL编码
            if isinstance(path, str):
                path = path.encode('utf-8')
            encoded = urlparse.quote(path, safe='/')
            raw_url = "https://raw.githubusercontent.com/%s/main/%s" % (REPO, encoded)
            return {"title": name, "url": raw_url}
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
    
    # 其他分类
    categories["desktop"] = get_latest("desktop")
    categories["mobile"] = get_latest("mobile")
    categories["avatar"] = get_latest("avatar")
    
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
