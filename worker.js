// Cloudflare Worker - 每日壁纸 API
// 部署到: https://wallpaper-api.adminlove520.workers.dev

export default {
  async fetch(request) {
    const url = new URL(request.url);
    
    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, OPTIONS',
    };
    
    if (url.pathname === '/api/latest') {
      const data = {
        date: new Date().toISOString().split('T')[0],
        generatedAt: new Date().toISOString(),
        categories: {
          // Bing - 从 Bing API 获取
          bing: await getBingWallpaper(),
          
          // Desktop - 手动指定示例（实际需要从网站获取）
          // TODO: 需要网站支持 API
          desktop: null,
          
          // Mobile - 手动指定示例
          mobile: null,
          
          // Avatar - 手动指定示例  
          avatar: null
        },
        note: "Bing 每日自动更新。其他分类需要网站支持 API。"
      };
      
      return new Response(JSON.stringify(data, null, 2), {
        headers: {
          ...corsHeaders,
          'Content-Type': 'application/json; charset=utf-8'
        }
      });
    }
    
    return new Response('Not Found', { status: 404 });
  }
};

async function getBingWallpaper() {
  try {
    const response = await fetch('https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN');
    const data = await response.json();
    const img = data.images[0];
    const urlbase = img.urlbase;
    
    return {
      title: img.title,
      copyright: img.copyright,
      date: img.startdate,
      url_1920x1080: `https://www.bing.com${urlbase}_1920x1080.jpg`,
      url_4k: `https://www.bing.com${urlbase}_UHD.jpg`
    };
  } catch (e) {
    return { title: '', url: '' };
  }
}
