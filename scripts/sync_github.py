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

# 确保输出是 UTF-8
if sys.version_info[0] >= 3:
    pass
else:
    reload(sys)
    sys.setdefaultencoding('utf-8')

def gh_tree(path, token=None):
    """使用 GitHub Tree API 获取文件列表"""
    # 使用 tree API 获取整个树
    url = "https://api.github.com/repos/%s/git/trees/main?recursive=1" % REPO
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    if token:
        req.add_header("Authorization", "token %s" % token)
    resp = urllib.request.urlopen(req, timeout=30)
    return json.loads(resp.read().decode('utf-8'))

def get_latest_by_prefix(prefix, token=None):
    """获取指定前缀目录下的最新文件"""
    try:
        data = gh_tree("", token)
        tree = data.get("tree", [])
        
        # 找到匹配的文件
        files = []
        for item in tree:
            if item.get("type") == "blob" and item["path"].startswith(prefix):
                files.append(item)
        
        if not files:
            return None
        
        # 按路径排序，取最新的
        files.sort(key=lambda x: x.get("sha", ""), reverse=True)
        latest = files[0]
        
        name = os.path.basename(latest["path"])
        title = name.rsplit(".", 1)[0] if "." in name else name
        
        # 构建 raw URL
        url = "https://raw.githubusercontent.com/%s/main/%s" % (REPO, latest["path"])
        
        return {"title": title, "url": url}
    except Exception as e:
        print("Error in %s: %s" % (prefix, e), flush=True)
        import traceback
        traceback.print_exc()
        return None

def main():
    token = os.environ.get("GH_TOKEN", None)
    
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
    
    # Desktop
    categories["desktop"] = get_latest_by_prefix("preview/desktop/", token)
    
    # Mobile
    categories["mobile"] = get_latest_by_prefix("preview/mobile/", token)
    
    # Avatar
    categories["avatar"] = get_latest_by_prefix("wallpaper/avatar/", token)
    
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
