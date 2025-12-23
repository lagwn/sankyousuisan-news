#!/usr/bin/env python3
"""
microCMS データエクスポートスクリプト
現在のサービスから全記事をエクスポートします
"""
import urllib.request
import urllib.error
import json
import csv

# 現在のサービス設定
SERVICE_DOMAIN = 'sankyou-suisan'
API_KEY = 'u3OWoP9egHtQhAmWO6KlNbNB2xzbPkSTH4hd'
ENDPOINT = 'news'

def get_all_articles():
    """全記事を取得（ページネーション対応）"""
    all_articles = []
    offset = 0
    limit = 100  # 1回のリクエストで取得する件数
    
    while True:
        url = f"https://{SERVICE_DOMAIN}.microcms.io/api/v1/{ENDPOINT}?limit={limit}&offset={offset}"
        
        req = urllib.request.Request(url, headers={
            'X-MICROCMS-API-KEY': API_KEY
        })
        
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode('utf-8'))
                articles = data.get('contents', [])
                total = data.get('totalCount', 0)
                
                # 新しい記事がなければ終了
                if not articles:
                    break
                
                all_articles.extend(articles)
                print(f"取得: {len(all_articles)}/{total}件")
                
                if len(all_articles) >= total:
                    break
                    
                offset += limit
                
        except urllib.error.HTTPError as e:
            print(f"エラー: {e.code} - {e.read().decode('utf-8')}")
            break
    
    return all_articles

def export_to_csv(articles, filename='export_data.csv'):
    """記事をCSVにエクスポート"""
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        # ヘッダー
        writer.writerow(['id', 'title', 'rawContent', 'richContent', 'postDate', 'publishedAt', 'createdAt'])
        
        for article in articles:
            writer.writerow([
                article.get('id', ''),
                article.get('title', ''),
                article.get('rawContent', ''),
                article.get('richContent', ''),
                article.get('postDate', ''),
                article.get('publishedAt', ''),
                article.get('createdAt', '')
            ])
    
    print(f"エクスポート完了: {filename}")

def export_to_json(articles, filename='export_data.json'):
    """記事をJSONにエクスポート（バックアップ用）"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    
    print(f"JSONバックアップ完了: {filename}")

def main():
    print("microCMSからデータをエクスポートしています...")
    print(f"サービス: {SERVICE_DOMAIN}")
    print(f"エンドポイント: {ENDPOINT}")
    print()
    
    articles = get_all_articles()
    
    if not articles:
        print("記事が見つかりませんでした")
        return
    
    print(f"\n合計 {len(articles)} 件の記事を取得しました")
    
    # CSVとJSONの両方でエクスポート
    export_to_csv(articles)
    export_to_json(articles)
    
    # 統計情報
    has_raw = sum(1 for a in articles if a.get('rawContent'))
    has_rich = sum(1 for a in articles if a.get('richContent'))
    has_date = sum(1 for a in articles if a.get('postDate'))
    
    print(f"\n--- 統計 ---")
    print(f"rawContent（HTML本文）あり: {has_raw}件")
    print(f"richContent（本文）あり: {has_rich}件")
    print(f"postDate（日付）あり: {has_date}件")

if __name__ == '__main__':
    main()
