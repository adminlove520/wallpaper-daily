# wallpaper-daily

每日壁纸数据自动同步仓库

## 数据接口

| 接口 | 地址 |
|------|------|
| 今日所有壁纸 | `https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json` |

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

- 每天 10:00 UTC 自动从 Bing API 获取最新数据
- 同时更新 `api/today.json`

## 其他分类说明

当前支持：
- ✅ Bing 每日壁纸（自动）

待支持（需要 wallpaper-gallery 网站 API）：
- ⏳ 电脑壁纸 (desktop)
- ⏳ 手机壁纸 (mobile)  
- ⏳ 头像 (avatar)

## 本地开发

```bash
# 安装依赖
pip install -r requirements.txt

# 运行同步脚本
python scripts/sync.py
```

## 贡献

欢迎提交 Issue 和 PR！
