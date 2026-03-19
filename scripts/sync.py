#!/usr/bin/env python3
"""
壁纸数据同步脚本 v3
从 wallpaper.061129.xyz CDN 获取最新壁纸数据
"""

import json
import urllib.request
import os
from datetime import datetime

# 配置
CDN_BASE = "https://wallpaper.061129.xyz/data"
OUTPUT_DIR = "api"

def fetch_json(url):
    """获取 JSON 数据"""
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.loads(response.read())

def get_bing_wallpaper():
    """获取今日 Bing 壁纸"""
    try:
        data = fetch_json(f"{CDN_BASE}/bing/latest.json")
        if data.get('items'):
            img = data['items'][0]
            urlbase = img['urlbase']
            return {
                "title": img['title'],
                "copyright": img['copyright'],
                "date": img['date'],
                "urlbase": urlbase,
                "url_1920x1080": f"https://www.bing.com{urlbase}_1920x1080.jpg",
                "url_4k": f"https://www.bing.com{urlbase}_UHD.jpg"
            }
    except Exception as e:
        print(f"Error fetching Bing: {e}")
    return {"title": "", "url_1920x1080": ""}

def generate_today_json(bing_data):
    """生成今日汇总 JSON"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    result = {
        "date": today,
        "generatedAt": datetime.now().isoformat() + "Z",
        "source": "https://wallpaper.061129.xyz",
        "categories": {
            "bing": bing_data,
            # TODO: 其他分类需要单独获取
            "desktop": None,
            "mobile": None,
            "avatar": None
        }
    }
    
    return result

def save_json(data, filename):
    """保存 JSON 文件"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"✓ Saved: {path}")

def main():
    print("=" * 50)
    print("壁纸数据同步 v3 (使用 CDN)")
    print("=" * 50)
    
    # 获取 Bing 壁纸
    print("\n[1] 获取 Bing 今日壁纸...")
    bing_data = get_bing_wallpaper()
    if bing_data.get('title'):
        print(f"  ✓ 今日壁纸: {bing_data['title']}")
    else:
        print("  ✗ 获取失败")
    
    # 生成今日汇总
    print("\n[2] 生成今日数据...")
    today_data = generate_today_json(bing_data)
    save_json(today_data, "today.json")
    
    print("\n" + "=" * 50)
    print("同步完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()
