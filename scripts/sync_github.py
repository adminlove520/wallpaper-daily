#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
自动同步壁纸数据
通过 GitHub API 获取最新文件
"""
import os
os.environ['PYTHONIOENCODING'] = 'utf-8'

import json
import urllib.request
from datetime import datetime
from urllib.parse import quote

REPO = "IT-NuanxinPro/nuanXinProPic"
BASE_URL = "https://api.github.com"

def gh_request(path):
    """GitHub API 请求"""
    url = f"{BASE_URL}/repos/{REPO}/{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    req.add_header("User-Agent", "wallpaper-sync-bot")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

def get_latest_by_category():
    """获取各分类最新文件"""
    categories = {}
    
    # Desktop
    try:
        desktop_contents = gh_request("contents/preview/desktop")
        latest_desktop = None
        latest_date = ""
        
        for item in desktop_contents:
            if item.get("type") != "dir":
                continue
            sub_contents = gh_request(f"contents/{item['path']}")
            for sub in sub_contents:
                if sub.get("type") != "file":
                    continue
                updated = sub.get("updated_at", "")
                if updated > latest_date:
                    latest_date = updated
                    latest_desktop = sub
        
        if latest_desktop:
            title = latest_desktop.get("name", "").rsplit(".", 1)[0]
            # 使用 URL 编码的 download_url
            path = latest_desktop.get("path", "")
            encoded_path = quote(path, safe='/')
            url = f"https://raw.githubusercontent.com/{REPO}/main/{encoded_path}"
            categories["desktop"] = {
                "title": title,
                "url": url
            }
    except Exception as e:
        print(f"Desktop error: {e}")
        categories["desktop"] = None
    
    # Mobile
    try:
        mobile_contents = gh_request("contents/preview/mobile")
        latest_mobile = None
        latest_date = ""
        
        for item in mobile_contents:
            if item.get("type") != "dir":
                continue
            sub_contents = gh_request(f"contents/{item['path']}")
            for sub in sub_contents:
                if sub.get("type") != "file":
                    continue
                updated = sub.get("updated_at", "")
                if updated > latest_date:
                    latest_date = updated
                    latest_mobile = sub
        
        if latest_mobile:
            title = latest_mobile.get("name", "").rsplit(".", 1)[0]
            path = latest_mobile.get("path", "")
            encoded_path = quote(path, safe='/')
            url = f"https://raw.githubusercontent.com/{REPO}/main/{encoded_path}"
            categories["mobile"] = {
                "title": title,
                "url": url
            }
    except Exception as e:
        print(f"Mobile error: {e}")
        categories["mobile"] = None
    
    # Avatar - 使用 wallpaper/avatar
    try:
        avatar_contents = gh_request("contents/wallpaper/avatar")
        latest_avatar = None
        latest_date = ""
        
        for item in avatar_contents:
            if item.get("type") != "dir":
                continue
            sub_contents = gh_request(f"contents/{item['path']}")
            for sub in sub_contents:
                if sub.get("type") != "file":
                    continue
                updated = sub.get("updated_at", "")
                if updated > latest_date:
                    latest_date = updated
                    latest_avatar = sub
        
        if latest_avatar:
            title = latest_avatar.get("name", "").rsplit(".", 1)[0]
            path = latest_avatar.get("path", "")
            encoded_path = quote(path, safe='/')
            url = f"https://raw.githubusercontent.com/{REPO}/main/{encoded_path}"
            categories["avatar"] = {
                "title": title,
                "url": url
            }
    except Exception as e:
        print(f"Avatar error: {e}")
        categories["avatar"] = None
    
    return categories

def main():
    print("获取最新壁纸数据...")
    
    # Bing - 使用 CDN
    try:
        bing_url = "https://wallpaper.061129.xyz/data/bing/latest.json"
        req = urllib.request.Request(bing_url)
        req.add_header("User-Agent", "wallpaper-sync-bot")
        bing_data = json.loads(urllib.request.urlopen(req, timeout=15).read().decode('utf-8'))
        bing_item = bing_data.get("items", [None])[0]
        if bing_item:
            urlbase = bing_item.get("urlbase", "")
            bing_url_final = f"https://www.bing.com{urlbase}_1920x1080.jpg"
            categories = {
                "bing": {
                    "title": bing_item.get("title", ""),
                    "url": bing_url_final
                }
            }
        else:
            categories = {"bing": None}
    except Exception as e:
        print(f"Bing error: {e}")
        categories = {"bing": None}
    
    # 其他分类 - GitHub API
    others = get_latest_by_category()
    categories.update(others)
    
    # 构建输出
    output = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "generatedAt": datetime.now().isoformat() + "Z",
        "categories": categories
    }
    
    print(json.dumps(output, ensure_ascii=False, indent=2))
    
    # 写入文件
    output_path = os.path.join(os.path.dirname(__file__), "..", "api", "today.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"已写入: {output_path}")

if __name__ == "__main__":
    main()
