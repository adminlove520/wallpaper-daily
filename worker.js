// Cloudflare Worker - 每日壁纸 API
// 部署: wrangler deploy worker.js

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, OPTIONS',
  'Content-Type': 'application/json; charset=utf-8',
};

const GITHUB_RAW = 'https://raw.githubusercontent.com/adminlove520/wallpaper-daily/main/api/today.json';

export default {
  async fetch(request) {
    const url = new URL(request.url);

    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: CORS_HEADERS });
    }

    if (url.pathname === '/api/latest') {
      return handleLatest();
    }

    if (url.pathname === '/api/category') {
      return handleCategory(url.searchParams.get('name'));
    }

    if (url.pathname === '/api/random') {
      return handleRandom();
    }

    return new Response(JSON.stringify({ error: 'Not Found' }), {
      status: 404,
      headers: CORS_HEADERS,
    });
  },
};

async function fetchData() {
  // Try GitHub RAW first (has full data from sync script)
  try {
    const res = await fetch(GITHUB_RAW, { cf: { cacheTtl: 3600 } });
    if (res.ok) return await res.json();
  } catch (_) {}

  // Fallback: fetch Bing directly
  const bing = await getBingWallpaper();
  return {
    date: new Date().toISOString().split('T')[0],
    generatedAt: new Date().toISOString(),
    categories: { bing, desktop: null, mobile: null, avatar: null },
  };
}

async function handleLatest() {
  const data = await fetchData();
  return new Response(JSON.stringify(data, null, 2), { headers: CORS_HEADERS });
}

async function handleCategory(name) {
  const valid = ['bing', 'desktop', 'mobile', 'avatar'];
  if (!name || !valid.includes(name.toLowerCase())) {
    return new Response(JSON.stringify({ error: 'Invalid category', valid }), {
      status: 400,
      headers: CORS_HEADERS,
    });
  }
  const data = await fetchData();
  const info = (data.categories || {})[name.toLowerCase()];
  if (!info || !info.url) {
    return new Response(JSON.stringify({ error: `No wallpaper for: ${name}` }), {
      status: 404,
      headers: CORS_HEADERS,
    });
  }
  return new Response(JSON.stringify({ date: data.date, category: name, ...info }, null, 2), {
    headers: CORS_HEADERS,
  });
}

async function handleRandom() {
  const data = await fetchData();
  const cats = data.categories || {};
  const entries = Object.entries(cats).filter(([, v]) => v && v.url);
  if (entries.length === 0) {
    return new Response(JSON.stringify({ error: 'No wallpapers available' }), {
      status: 404,
      headers: CORS_HEADERS,
    });
  }
  const [category, info] = entries[Math.floor(Math.random() * entries.length)];
  return new Response(JSON.stringify({ date: data.date, category, ...info }, null, 2), {
    headers: CORS_HEADERS,
  });
}

async function getBingWallpaper() {
  try {
    const res = await fetch('https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1&mkt=zh-CN');
    const data = await res.json();
    const img = data.images[0];
    return {
      title: img.title,
      url: `https://www.bing.com${img.urlbase}_1920x1080.jpg`,
    };
  } catch (_) {
    return null;
  }
}
