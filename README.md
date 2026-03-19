# wallpaper-daily

每日壁纸数据自动同步仓库

## 数据接口

| 接口 | 地址 |
|------|------|
| 今日所有壁纸 | `https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json` |
| 桌面壁纸 | `https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/desktop.json` |
| 手机壁纸 | `https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/mobile.json` |
| 头像 | `https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/avatar.json` |

## 数据格式

```json
{
  "date": "2026-03-19",
  "generatedAt": "2026-03-19T10:00:00Z",
  "categories": {
    "bing": {
      "title": "激发你的好奇心",
      "copyright": "澳洲针鼹，阿德莱德山，澳大利亚",
      "url": "https://www.bing.com/th?id=OHR.xxx_1920x1080.jpg"
    },
    "desktop": {
      "title": "彩虹发色的梦幻少女仰望星空",
      "category": "动漫/二次元",
      "url": "https://cdn.jsdelivr.net/gh/..."
    }
  }
}
```

## 自动同步

- 每天 10:00 UTC 自动从 Bing API 获取最新数据
- 同时更新所有分类的最新壁纸链接
