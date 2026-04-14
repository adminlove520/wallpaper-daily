# wallpaper-daily

每日壁纸数据自动同步 — Bing / Desktop / Mobile / Avatar

每天自动从 [Bing](https://www.bing.com) 和 [nuanXinProPic](https://github.com/IT-NuanxinPro/nuanXinProPic) 抓取最新壁纸，通过 GitHub Actions 同步到 JSON，并提供 Vercel API。

## API 接口

### 获取全部分类

```
GET https://wallpaper-daily.vercel.app/api/latest
GET https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json
```

返回示例：

```json
{
  "date": "2026-04-14",
  "generatedAt": "2026-04-14T02:00:00Z",
  "categories": {
    "bing":    { "title": "...", "url": "https://www.bing.com/th?id=..." },
    "desktop": { "title": "...", "url": "https://cdn.jsdelivr.net/gh/..." },
    "mobile":  { "title": "...", "url": "https://cdn.jsdelivr.net/gh/..." },
    "avatar":  { "title": "...", "url": "https://cdn.jsdelivr.net/gh/..." }
  }
}
```

### 按分类获取

```
GET /api/category?name=bing
GET /api/category?name=desktop
GET /api/category?name=mobile
GET /api/category?name=avatar
```

### 随机壁纸

```
GET /api/random
```

## 快速部署

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/import?repo=adminlove520/wallpaper-daily)

或手动部署：

```bash
npm i -g vercel
cd wallpaper-daily
vercel login
vercel --prod
```

## 壁纸分类

| 分类 | 来源 | 更新频率 |
|------|------|----------|
| `bing` | Bing 每日壁纸 | 每日 |
| `desktop` | nuanXinProPic 桌面壁纸 | 每日 |
| `mobile` | nuanXinProPic 手机壁纸 | 每日 |
| `avatar` | nuanXinProPic 头像 | 每日 |

## 使用示例

```python
import urllib.request, json

url = "https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json"
data = json.loads(urllib.request.urlopen(url).read())

for cat, info in data['categories'].items():
    if info:
        print(f"{cat}: {info['title']}")
        print(f"  URL: {info['url']}")
```

## 文件结构

```
wallpaper-daily/
├── api/
│   ├── today.json      # 今日壁纸数据（GitHub Actions 自动更新）
│   ├── latest.js       # Vercel API — 获取全部分类
│   ├── category.js     # Vercel API — 按分类获取
│   └── random.js       # Vercel API — 随机壁纸
├── scripts/
│   ├── sync_github.py      # 数据同步脚本
│   └── post_discussion.py  # GitHub Discussion 推送
├── .github/workflows/
│   ├── daily.yml           # 每日同步 (02:00 UTC)
│   └── post-discussion.yml # Discussion 推送 (10:00 UTC)
├── worker.js           # Cloudflare Worker 备用方案
├── vercel.json         # Vercel 配置
├── package.json
└── README.md
```

## 自动化流程

```
GitHub Actions (daily.yml)
    ↓ cron 02:00 UTC
sync_github.py
    ↓ 抓取 Bing + nuanXinProPic
api/today.json (更新)
    ↓ git push
Vercel (自动部署)
    ↓
/api/latest → 返回 JSON
```

---

## 参与贡献

欢迎提交 Issue 和 PR！
