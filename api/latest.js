// Vercel Serverless API
// 文件路径: api/latest.js
// 部署后访问: https://wallpaper-daily.vercel.app/api/latest

export default async function handler(req, res) {
  // 设置 CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  try {
    // 获取 Bing 今日壁纸
    const bingResponse = await fetch('https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN');
    const bingData = await bingResponse.json();
    const img = bingData.images[0];
    const urlbase = img.urlbase;
    
    const data = {
      date: new Date().toISOString().split('T')[0],
      generatedAt: new Date().toISOString(),
      categories: {
        bing: {
          title: img.title,
          copyright: img.copyright,
          date: img.startdate,
          urlbase: urlbase,
          url_1920x1080: `https://www.bing.com${urlbase}_1920x1080.jpg`,
          url_4k: `https://www.bing.com${urlbase}_UHD.jpg`
        },
        // TODO: 其他分类需要从 wallpaper-gallery 网站获取
        desktop: null,
        mobile: null,
        avatar: null
      },
      note: "Bing 每日自动更新。其他分类需要 wallpaper-gallery 网站支持 API。"
    };
    
    return res.status(200).json(data);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
