#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动同步壁纸数据
通过 GitHub API 获取最新文件
"""
from __future__ import print_function
import os
import sys

# 强制 UTF-8 编码
if sys.version_info[0] < 3:
    reload(sys)
    sys.setdefaultencoding('utf-8')
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import urllib.request
from datetime import datetime
from urllib.parse import quote

REPO = "IT-NuanxinPro/nuanXinProPic"
BASE_URL = "https://api.github.com"

def gh_request(path):
    """GitHub API 请求"""
    url = "%s/repos/%s/%s" % (BASE_URL, REPO, path)
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "wallpaper-sync-bot")
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode('utf-8'))

def get_latest_file(path_prefix):
    """获取目录下最新文件"""
    try:
        contents = gh_request("contents/" + path_prefix)
        latest = None
        latest_date = ""
        
        for item in contents:
            if item.get("type") != "dir":
                continue
            sub_contents = gh_request("contents/" + item["path"])
            for sub in sub_contents:
                if sub.get("type") != "file":
                    continue
                updated = sub.get("updated_at", "")
                if updated > latest_date:
                    latest_date = updated
                    latest = sub
        
        if latest:
            title = latest.get("name", "").rsplit(".", 1)[0]
            # 手动 URL 编码路径
            path = latest.get("path", "")
            parts = path.split('/')
            encoded_parts = [quote(p.encode('utf-8')) for p in parts]
            encoded_path = '/'.join(encoded_parts)
            url = "https://raw.githubusercontent.com/%s/main/%s" % (REPO, encoded_path)
            return {"title": title, "url": url}
    except Exception as e:
        print("Error in %s: %s" % (path_prefix, e), flush=True)
    
    return None

def main():
    print("获取最新壁纸数据...", flush=True)
    categories = {}
    
    # Bing - 使用 CDN
    try:
        bing_url = "https://wallpaper.061129.xyz/data/bing/latest.json"
        req = urllib.request.Request(bing_url)
        req.add_header("User-Agent", "wallpaper-sync-bot")
        bing_data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))
        bing_item = bing_data.get("items", [None])[0]
        if bing_item:
            urlbase = bing_item.get("urlbase", "")
            bing_url_final = "https://www.bing.com%s_1920x1080.jpg" % urlbase
            categories["bing"] = {
                "title": bing_item.get("title", ""),
                "url": bing_url_final
            }
        else:
            categories["bing"] = None
    except Exception as e:
        print("Bing error: %s" % e, flush=True)
        categories["bing"] = None
    
    # 其他分类
    categories["desktop"] = get_latest_file("preview/desktop")
    categories["mobile"] = get_latest_file("preview/mobile")
    categories["avatar"] = get_latest_file("wallpaper/avatar")
    
    # 构建输出
    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "generatedAt": datetime.now().isoformat() + "Z",
        "categories": categories
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2), flush=True)
    
    # 写入文件
    output_path = os.path.join(os.path.dirname(__file__), "..", "api", "today.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print("已写入: %s" % output_path, flush=True)

if __name__ == "__main__":
    main()
