import { readFileSync } from 'fs';
import { join } from 'path';

export default function handler(req, res) {
  // 设置 CORS
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, OPTIONS');
  
  if (req.method === 'OPTIONS') {
    return res.status(200).end();
  }
  
  try {
    // 读取静态 JSON 文件
    const data = JSON.parse(
      readFileSync(join(process.cwd(), 'api', 'today.json'), 'utf-8')
    );
    
    return res.status(200).json(data);
  } catch (error) {
    return res.status(500).json({ error: error.message });
  }
}
