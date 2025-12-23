# 三共水産 ニュースCMSシステム（HTML/CSS/JS版）

microCMSをヘッドレスCMSとして使用した、静的HTMLベースのニュースページシステムです。

## ディレクトリ構成

```
news/
├── index.html     # 一覧ページ
├── detail.html    # 詳細ページ
├── vercel.json    # Vercel設定
├── css/
│   └── style.css  # コンパイル済みCSS
├── scss/
│   ├── style.scss      # メインSCSS
│   └── _variables.scss # SCSS変数
├── js/
│   ├── config.js    # microCMS設定 ★要編集
│   ├── microcms.js  # API連携
│   ├── list.js      # 一覧ページ用
│   └── detail.js    # 詳細ページ用
└── img/             # 画像リソース
```

## セットアップ手順

### 1. microCMSの設定

1. [microCMS](https://microcms.io/)でアカウント作成
2. 新しいサービスを作成
3. APIを作成:
   - **API名**: news
   - **エンドポイント**: news
   - **型**: リスト形式
4. フィールドを設定:
   - `title`（テキストフィールド）
   - `content`（リッチエディタ）

### 2. APIキーの設定

`js/config.js` を編集:

```javascript
const MICROCMS_CONFIG = {
  serviceDomain: 'YOUR_SERVICE_DOMAIN',  // ← 変更
  apiKey: 'YOUR_API_KEY',                // ← 変更
  endpoint: 'news'
};
```

> ⚠️ **重要**: 公開用APIキー（GETのみ許可）を使用してください。
> microCMS管理画面 > サービス設定 > APIキー > 「権限」を「GET」のみに設定

### 3. 画像リソースの配置

`img/`フォルダに以下のファイルを配置:
- favicon.ico
- close.gif
- alpha_bg.jpg
- topics.jpg
- icn_arrow.gif
- entry_bg.gif
- vector_red_02.gif

### 4. ローカル確認

ローカルサーバーで確認（CORSの都合上、直接HTMLファイルを開くとAPIが動作しません）:

```bash
# Python 3の場合
cd /Volumes/T7/三共水産/www/news
python3 -m http.server 8000

# または npx serve
npx -y serve .
```

http://localhost:8000 でアクセス

## Vercelへのデプロイ

### 1. Vercelでプロジェクト作成

1. [Vercel](https://vercel.com)にログイン
2. 「New Project」→ このディレクトリをインポート
3. Framework Preset: 「Other」を選択
4. デプロイ

### 2. ドメイン設定

1. Vercelダッシュボード > プロジェクト > Settings > Domains
2. `www2.sankyou-suisan.co.jp` を追加
3. DNS設定:
   - **CNAME**: `cname.vercel-dns.com`
   - または **A**: `76.76.21.21`

## SCSSのコンパイル

SCSSを編集した場合、以下でCSSを再生成:

```bash
npx sass scss/style.scss css/style.css
```

自動監視モード:
```bash
npx sass --watch scss/style.scss:css/style.css
```

## URL構成

- **一覧ページ**: `https://www2.sankyou-suisan.co.jp/news/`
- **詳細ページ**: `https://www2.sankyou-suisan.co.jp/news/detail.html?id=記事ID`
