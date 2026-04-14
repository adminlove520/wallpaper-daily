# 每日壁纸 API 部署指南

## 方案一：Vercel 部署（推荐）

### 1. 一键部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/import?repo=adminlove520/wallpaper-daily)

### 2. 手动部署

```bash
npm i -g vercel
cd wallpaper-daily
vercel login
vercel --prod
```

### 3. API 端点

| 端点 | 说明 |
|------|------|
| `/api/latest` | 获取全部分类壁纸 |
| `/api/category?name=bing` | 按分类获取（bing/desktop/mobile/avatar） |
| `/api/random` | 随机返回一个分类的壁纸 |

---

## 方案二：GitHub RAW（无需部署）

```
https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json
```

数据由 GitHub Actions 每日 02:00 UTC 自动同步。

---

## 方案三：Cloudflare Worker

使用 `worker.js` 部署到 Cloudflare Workers，实时从 Bing 获取壁纸。

```bash
wrangler deploy worker.js
```

---

## 使用示例

```python
import urllib.request, json

# GitHub RAW（推荐，无需部署）
url = "https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json"

# 或 Vercel API
# url = "https://wallpaper-daily-iota.vercel.app/api/latest"

data = json.loads(urllib.request.urlopen(url).read())

for cat, info in data['categories'].items():
    if info:
        print(f"{cat}: {info['title']}")
        print(f"  URL: {info['url']}")
```
