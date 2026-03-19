#!/usr/bin/env python3
"""
自动同步壁纸数据
通过 GitHub API 获取最新文件
"""

import json
import os
import urllib.request
from datetime import datetime

REPO = "IT-NuanxinPro/nuanXinProPic"
BASE_URL = "https://api.github.com"

def gh_request(path):
    """GitHub API 请求"""
    url = f"{BASE_URL}/repos/{REPO}/{path}"
    req = urllib.request.Request(url)
    req.add_header("Accept", "application/vnd.github.v3+json")
    # 添加 User-Agent 避免限流
    req.add_header("User-Agent", "wallpaper-sync-bot")
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read())

def get_latest_file(path_prefix):
    """获取目录下最新文件"""
    # 获取目录内容
    contents = gh_request(f"contents/{path_prefix}")
    
    # 遍历子目录找最新文件
    latest_file = None
    latest_date = None
    
    for item in contents:
        if item["type"] != "dir":
            continue
        # 获取子目录内容
        sub_contents = gh_request(f"contents/{item['path']}")
        for sub in sub_contents:
            if sub["type"] != "file":
                continue
            # 获取文件信息
            file_info = gh_request(f"contents/{sub['path']}")
            date = file_info.get("updated_at", "")
            if latest_date is None or date > latest_date:
                latest_date = date
                latest_file = {
                    "name": sub["name"],
                    "path": sub["path"],
                    "download_url": sub["download_url"]
                }
    
    return latest_file

def get_latest_by_category():
    """获取各分类最新文件"""
    categories = {}
    
    # Desktop - 找最新
    try:
        # 遍历所有子目录找最新
        desktop_contents = gh_request("contents/preview/desktop")
        latest_desktop = None
        latest_date = None
        
        for item in desktop_contents:
            if item["type"] != "dir":
                continue
            sub_contents = gh_request(f"contents/{item['path']}")
            for sub in sub_contents:
                if sub["type"] != "file":
                    continue
                # 比较更新时间
                if latest_date is None or sub.get("updated_at", "") > latest_date:
                    latest_date = sub.get("updated_at", "")
                    latest_desktop = sub
        
        if latest_desktop:
            categories["desktop"] = {
                "title": latest_desktop["name"].rsplit(".", 1)[0],
                "url": latest_desktop["download_url"]
            }
    except Exception as e:
        print(f"Desktop error: {e}")
        categories["desktop"] = None
    
    # Mobile
    try:
        mobile_contents = gh_request("contents/preview/mobile")
        latest_mobile = None
        latest_date = None
        
        for item in mobile_contents:
            if item["type"] != "dir":
                continue
            sub_contents = gh_request(f"contents/{item['path']}")
            for sub in sub_contents:
                if sub["type"] != "file":
                    continue
                if latest_date is None or sub.get("updated_at", "") > latest_date:
                    latest_date = sub.get("updated_at", "")
                    latest_mobile = sub
        
        if latest_mobile:
            categories["mobile"] = {
                "title": latest_mobile["name"].rsplit(".", 1)[0],
                "url": latest_mobile["download_url"]
            }
    except Exception as e:
        print(f"Mobile error: {e}")
        categories["mobile"] = None
    
    # Avatar - 使用 wallpaper/avatar
    try:
        avatar_contents = gh_request("contents/wallpaper/avatar")
        latest_avatar = None
        latest_date = None
        
        for item in avatar_contents:
            if item["type"] != "dir":
                continue
            sub_contents = gh_request(f"contents/{item['path']}")
            for sub in sub_contents:
                if sub["type"] != "file":
                    continue
                if latest_date is None or sub.get("updated_at", "") > latest_date:
                    latest_date = sub.get("updated_at", "")
                    latest_avatar = sub
        
        if latest_avatar:
            categories["avatar"] = {
                "title": latest_avatar["name"].rsplit(".", 1)[0],
                "url": latest_avatar["download_url"]
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
        bing_data = json.loads(urllib.request.urlopen(req, timeout=15).read())
        bing_item = bing_data["items"][0] if bing_data.get("items") else None
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
