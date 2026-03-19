# 每日壁纸 API 部署指南

## 方案一：Vercel 部署（推荐）

### 1. 部署

点击下方按钮一键部署：

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/import?repo=adminlove520/wallpaper-daily)

或者手动部署：

```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 进入目录
cd wallpaper-daily

# 3. 登录
vercel login

# 4. 部署
vercel
```

### 2. 使用

部署后访问：`https://your-project.vercel.app/api/latest`

### 3. 更新数据

修改 `api/latest.js` 中的数据，然后：
```bash
vercel --prod
```

---

## 方案二：GitHub RAW（当前可用）

直接使用 GitHub 仓库的 RAW 文件：

```
https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json
```

**注意**：这个文件需要 GitHub Actions 自动同步才能保持最新。

---

## 方案三：手动更新 JSON

### 1. 获取今日壁纸数据

访问壁纸网站获取各分类最新图片：
- 电脑壁纸：https://wallpaper.dfyx.click/desktop
- 每日Bing：https://wallpaper.dfyx.click/bing
- 手机壁纸：https://wallpaper.dfyx.click/mobile
- 头像：https://wallpaper.dfyx.click/avatar

### 2. 更新 JSON 文件

编辑 `wallpaper-daily/api/today.json`：

```json
{
  "date": "2026-03-19",
  "generatedAt": "2026-03-19T03:00:00Z",
  "categories": {
    "bing": {
      "title": "激发你的好奇心",
      "url": "https://www.bing.com/th?id=OHR.xxx_1920x1080.jpg"
    },
    "desktop": {
      "title": "图片标题",
      "url": "https://cdn.jsdelivr.net/gh/..."
    },
    "mobile": {...},
    "avatar": {...}
  }
}
```

### 3. 提交并推送

```bash
git add .
git commit -m "feat: 更新今日壁纸"
git push
```

---

## 小溪使用方式

```python
import urllib.request, json

# 方式一：GitHub RAW
url = "https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json"

# 方式二：Vercel（部署后）
url = "https://your-project.vercel.app/api/latest"

data = json.loads(urllib.request.urlopen(url).read())

# 获取所有分类
for cat, info in data['categories'].items():
    if info:
        print(f"{cat}: {info['title']}")
        print(f"  URL: {info['url']}")
```

---

## 文件结构

```
wallpaper-daily/
├── api/
│   ├── today.json      # 今日壁纸数据
│   └── latest.js       # Vercel Serverless Function
├── scripts/
│   └── sync.py         # 同步脚本
├── vercel.json         # Vercel 配置
└── README.md
```

---

有问题随时问！🦞
