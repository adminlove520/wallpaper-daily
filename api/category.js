const fs = require('fs');
const path = require('path');

const VALID_CATEGORIES = ['bing', 'desktop', 'mobile', 'avatar'];

module.exports = function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Cache-Control', 's-maxage=3600, stale-while-revalidate=86400');

  if (req.method === 'OPTIONS') return res.status(200).end();

  const cat = (req.query.name || '').toLowerCase();
  if (!cat || !VALID_CATEGORIES.includes(cat)) {
    return res.status(400).json({
      error: 'Invalid category',
      valid: VALID_CATEGORIES
    });
  }

  try {
    const jsonPath = path.join(__dirname, 'today.json');
    const data = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
    const info = (data.categories || {})[cat];

    if (!info || !info.url) {
      return res.status(404).json({ error: `No wallpaper for category: ${cat}` });
    }

    return res.status(200).json({ date: data.date, category: cat, ...info });
  } catch (error) {
    return res.status(500).json({
      error: 'Failed to load wallpaper data',
      message: error.message
    });
  }
};
