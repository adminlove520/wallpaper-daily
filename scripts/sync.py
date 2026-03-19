#!/usr/bin/env python3
"""
壁纸数据同步脚本 v2
从多个数据源获取最新壁纸数据
"""

import json
import urllib.request
import os
from datetime import datetime

# 配置
BING_API_URL = "https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN"
WALLPAPER_GALLERY_DATA = "https://raw.githubusercontent.com/adminlove520/wallpaper-gallery/main/public/data"
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
        print(f"Error fetching Bing: {e}")
        return {"title": "", "url_1920x1080": ""}

def generate_today_json(bing_data):
    """生成今日汇总 JSON"""
    today = datetime.now().strftime("%Y-%m-%d")
    
    result = {
        "date": today,
        "generatedAt": datetime.now().isoformat() + "Z",
        "categories": {
            "bing": bing_data,
            # 其他分类暂时无法自动获取
            # 需要 wallpaper-gallery 网站支持 API
            "desktop": None,
            "mobile": None,
            "avatar": None
        },
        "note": "Bing 每日自动更新。其他分类需要 wallpaper-gallery 网站支持 API。"
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
    print("壁纸数据同步 v2")
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
    
    print("\n注意: 其他分类 (desktop/mobile/avatar) 需要")
    print("wallpaper-gallery 网站添加 API 支持才能自动获取。")

if __name__ == "__main__":
    main()
