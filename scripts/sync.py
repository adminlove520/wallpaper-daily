#!/usr/bin/env python3
"""
壁纸数据同步脚本
从 Bing API 获取最新壁纸数据，生成统一的 JSON 文件
"""

import json
import urllib.request
import os
from datetime import datetime

BING_API_URL = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN"
OUTPUT_DIR = "api"

def get_bing_wallpaper():
    """获取今日 Bing 壁纸"""
    try:
        with urllib.request.urlopen(BING_API_URL, timeout=10) as response:
            data = json.loads(response.read())
        
        img = data['images'][0]
        urlbase = img['urlbase']
        
        return {
            "title": img['title'],
            "copyright": img['copyright'],
            "date": img['startdate'],
            "urlbase": urlbase,
            "url_1920x1080": f"https://www.bing.com{urlbase}_1920x1080.jpg",
            "url_4k": f"https://www.bing.com{urlbase}_UHD.jpg"
        }
    except Exception as e:
        print(f"Error fetching Bing wallpaper: {e}")
        return None

def generate_today_json(bing_data):
    """生成今日汇总 JSON"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    result = {
        "date": today,
        "generatedAt": datetime.now().isoformat() + "Z",
        "categories": {
            "bing": bing_data
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
    print("壁纸数据同步开始")
    print("=" * 50)
    
    # 获取 Bing 壁纸
    print("\n[1/2] 获取 Bing 今日壁纸...")
    bing_data = get_bing_wallpaper()
    if bing_data:
        print(f"  ✓ 今日壁纸: {bing_data['title']}")
    else:
        print("  ✗ 获取失败，使用空数据")
        bing_data = {
            "title": "",
            "copyright": "",
            "date": "",
            "url": ""
        }
    
    # 生成今日汇总
    print("\n[2/2] 生成今日数据...")
    today_data = generate_today_json(bing_data)
    save_json(today_data, "today.json")
    
    print("\n" + "=" * 50)
    print("同步完成!")
    print("=" * 50)

if __name__ == "__main__":
    main()
