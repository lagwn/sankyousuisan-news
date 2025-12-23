/**
 * 画像プロキシAPI
 * HTTP画像をHTTPS経由で配信するためのサーバーレス関数
 */

export default async function handler(req, res) {
    const { url } = req.query;

    if (!url) {
        return res.status(400).json({ error: 'URL parameter is required' });
    }

    try {
        // URLをデコード
        const imageUrl = decodeURIComponent(url);

        // 許可されたドメインのみ処理
        const allowedDomains = [
            'www2.sankyou-suisan.co.jp',
            'sankyou-suisan.co.jp'
        ];

        const urlObj = new URL(imageUrl);
        if (!allowedDomains.some(domain => urlObj.hostname.includes(domain))) {
            return res.status(403).json({ error: 'Domain not allowed' });
        }

        // 画像を取得
        const response = await fetch(imageUrl);

        if (!response.ok) {
            return res.status(response.status).json({ error: 'Failed to fetch image' });
        }

        // Content-Typeを取得
        const contentType = response.headers.get('content-type') || 'image/jpeg';

        // バッファとして取得
        const buffer = await response.arrayBuffer();

        // キャッシュヘッダーを設定（1日）
        res.setHeader('Cache-Control', 'public, max-age=86400, s-maxage=86400');
        res.setHeader('Content-Type', contentType);

        // 画像データを返す
        return res.send(Buffer.from(buffer));

    } catch (error) {
        console.error('Proxy error:', error);
        return res.status(500).json({ error: 'Internal server error' });
    }
}
