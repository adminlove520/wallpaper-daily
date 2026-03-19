# wallpaper-daily

每日壁纸数据自动同步仓库

## 数据接口

| 接口 | 地址 |
|------|------|
| 今日所有壁纸 | `https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json` |

> ⚠️ 注意：由于技术限制，当前只支持 Bing 每日自动更新。

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

## 自动同步

- ✅ 每天 10:00 UTC 自动从 Bing API 获取最新数据
- ⏳ 其他分类需要 wallpaper-gallery 网站支持 API

## 其他分类解决方案

### 方案：在 wallpaper-gallery 添加 API

在网站添加 `/api/latest` 接口，返回所有分类的最新壁纸：

```json
{
  "date": "2026-03-19",
  "categories": {
    "bing": { "title": "...", "url": "..." },
    "desktop": { "title": "...", "url": "..." },
    "mobile": { "title": "...", "url": "..." },
    "avatar": { "title": "...", "url": "..." }
  }
}
```

然后小溪就能直接调用这个 API 了！

### 实现方式

1. **Cloudflare Workers**（推荐）
2. **静态 JSON + GitHub Actions 定时更新**
3. **网站构建时生成**

---

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

---

## 参与贡献

欢迎提交 Issue 和 PR！
