const fs = require('fs');
const path = require('path');

module.exports = function handler(req, res) {
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  res.setHeader('Cache-Control', 's-maxage=60, stale-while-revalidate=300');

  if (req.method === 'OPTIONS') return res.status(200).end();

  try {
    const jsonPath = path.join(__dirname, 'today.json');
    const data = JSON.parse(fs.readFileSync(jsonPath, 'utf-8'));
    const cats = data.categories || {};
    const valid = Object.entries(cats).filter(([, v]) => v && v.url);

    if (valid.length === 0) {
      return res.status(404).json({ error: 'No wallpapers available' });
    }

    const [category, info] = valid[Math.floor(Math.random() * valid.length)];
    return res.status(200).json({ date: data.date, category, ...info });
  } catch (error) {
    return res.status(500).json({
      error: 'Failed to load wallpaper data',
      message: error.message
    });
  }
};
