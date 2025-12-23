#!/usr/bin/env python3
"""
microCMS API一括インポートスクリプト
CSVからHTMLを保持したままデータをインポートします
"""
import urllib.request
import urllib.error
import json
import csv
import time

SERVICE_DOMAIN = 'sankyou-suisan'
API_KEY = 'u3OWoP9egHtQhAmWO6KlNbNB2xzbPkSTH4hd'
ENDPOINT = 'news'

def create_article(content_id, title, content, post_date):
    """記事を作成（PUT: IDを指定して作成）"""
    url = f"https://{SERVICE_DOMAIN}.microcms.io/api/v1/{ENDPOINT}/{content_id}"
    
    data = {
        'title': title,
        'rawContent': content,
    }
    
    # postDateがある場合は追加
    if post_date:
        data['postDate'] = post_date
    
    json_data = json.dumps(data).encode('utf-8')
    
    req = urllib.request.Request(url, data=json_data, headers={
        'X-MICROCMS-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }, method='PUT')
    
    try:
        with urllib.request.urlopen(req) as res:
            return True, None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return False, f"{e.code}: {error_body}"

def main():
    print("CSVファイルを読み込んでいます...")
    
    articles = []
    with open('microcms_import_fixed.csv', 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)  # Skip header
        for row in reader:
            if len(row) >= 4:
                articles.append({
                    'id': row[0],
                    'title': row[1],
                    'content': row[2],
                    'postDate': row[3]
                })
    
    print(f"{len(articles)}件の記事を読み込みました")
    
    # HTMLタグの確認
    img_count = sum(1 for a in articles if '<img' in a['content'])
    link_count = sum(1 for a in articles if '<a' in a['content'])
    print(f"  - 画像を含む記事: {img_count}件")
    print(f"  - リンクを含む記事: {link_count}件")
    
    print(f"\n{len(articles)}件の記事をインポートします...")
    
    success = 0
    failed = 0
    
    for i, article in enumerate(articles):
        ok, error = create_article(
            article['id'],
            article['title'],
            article['content'],
            article['postDate']
        )
        
        if ok:
            success += 1
            print(f"[{i+1}/{len(articles)}] ✓ {article['id']}: {article['title'][:30]}")
        else:
            failed += 1
            print(f"[{i+1}/{len(articles)}] ✗ {article['id']}: {error}")
        
        # API制限を避けるため少し待機
        time.sleep(0.3)
    
    print(f"\n完了: 成功 {success}件 / 失敗 {failed}件")

if __name__ == '__main__':
    main()
