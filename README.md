# wallpaper-daily

每日壁纸数据自动同步仓库

## 数据接口

### 方式一：GitHub RAW（当前可用）
```
https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json
```

### 方式二：Vercel API（需要部署）
```
https://wallpaper-daily.vercel.app/api/latest
```

> ⚠️ 注意：由于技术限制，当前只支持 Bing 每日自动更新。

## 快速部署到 Vercel

```bash
# 1. 安装 Vercel CLI
npm i -g vercel

# 2. 进入目录
cd wallpaper-daily

# 3. 登录
vercel login

# 4. 部署
vercel

# 5. 之后每次更新
vercel --prod
```

部署后访问：`https://your-project.vercel.app/api/latest`

## 数据格式

```json
{
  "date": "2026-03-19",
  "generatedAt": "2026-03-19T10:00:00Z",
  "categories": {
    "bing": {
      "title": "激发你的好奇心",
      "url_1920x1080": "https://www.bing.com/th?id=OHR.xxx_1920x1080.jpg",
      "url_4k": "https://www.bing.com/th?id=OHR.xxx_UHD.jpg"
    },
    "desktop": null,
    "mobile": null,
    "avatar": null
  },
  "note": "Bing 每日自动更新。其他分类需要 wallpaper-gallery 网站支持 API。"
}
```

## 其他分类解决方案

### 方案：在 wallpaper-gallery 添加 API

在网站添加 `/api/latest` 接口，返回所有分类的最新壁纸。

## 使用示例

```python
import urllib.request, json

url = "https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json"
data = json.loads(urllib.request.urlopen(url).read())

# 获取 Bing 今日壁纸
bing = data['categories']['bing']
print(f"今日壁纸: {bing['title']}")
print(f"链接: {bing['url_1920x1080']}")
```

## 文件结构

```
wallpaper-daily/
├── api/
│   ├── today.json      # GitHub RAW 使用的静态文件
│   └── latest.js       # Vercel Serverless Function
├── scripts/
│   └── sync.py         # 同步脚本
├── worker.js           # Cloudflare Worker 模板
├── vercel.json         # Vercel 配置
└── README.md
```

---

## 参与贡献

欢迎提交 Issue 和 PR！
