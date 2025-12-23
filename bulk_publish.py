#!/usr/bin/env python3
"""
microCMS 一括公開スクリプト（修正版2）
既存のtitleで更新して公開する
"""
import urllib.request
import urllib.error
import json
import time

SERVICE_DOMAIN = 'sankyou-suisan'
API_KEY = 'u3OWoP9egHtQhAmWO6KlNbNB2xzbPkSTH4hd'
ENDPOINT = 'news'

def get_all_contents():
    """全記事を取得"""
    all_contents = []
    offset = 0
    limit = 100
    
    while True:
        url = f"https://{SERVICE_DOMAIN}.microcms.io/api/v1/{ENDPOINT}?limit={limit}&offset={offset}"
        req = urllib.request.Request(url, headers={'X-MICROCMS-API-KEY': API_KEY})
        
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode('utf-8'))
                contents = data.get('contents', [])
                all_contents.extend(contents)
                if len(contents) < limit:
                    break
                offset += limit
        except urllib.error.HTTPError as e:
            print(f"取得エラー: {e.code}")
            break
    
    return all_contents

def publish_article(content_id, title):
    """記事を公開（titleを再送信して公開）"""
    url = f"https://{SERVICE_DOMAIN}.microcms.io/api/v1/{ENDPOINT}/{content_id}"
    
    # titleを再送信（これで公開される）
    data = json.dumps({'title': title}).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={
        'X-MICROCMS-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }, method='PATCH')
    
    try:
        with urllib.request.urlopen(req) as res:
            return True
    except urllib.error.HTTPError as e:
        print(f"  エラー: {content_id} - {e.code}")
        return False

def main():
    print("記事を取得中...")
    articles = get_all_contents()
    
    if not articles:
        print("記事が見つかりません")
        return
    
    print(f"{len(articles)}件の記事を公開します...")
    
    success = 0
    for i, article in enumerate(articles):
        content_id = article['id']
        title = article.get('title', '')
        
        if publish_article(content_id, title):
            success += 1
            print(f"[{i+1}/{len(articles)}] 公開: {title[:25]}")
        
        time.sleep(0.3)
    
    print(f"\n完了: {success}/{len(articles)}件を公開しました")

if __name__ == '__main__':
    main()
