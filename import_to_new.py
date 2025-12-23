#!/usr/bin/env python3
"""
新しいmicroCMSサービスへのインポートスクリプト
エクスポートしたデータを新サービスにインポートします
"""
import urllib.request
import urllib.error
import json
import time

# 新しいサービス設定
SERVICE_DOMAIN = 'sankyousuisan'
API_KEY = 'YlPZ9U71HoGRKig8GWJ0PXrGlTV6ttn3Hb6S'
ENDPOINT = 'news'

def create_article(article_data):
    """記事を作成（PUT: IDを指定して作成）"""
    content_id = article_data['id']
    url = f"https://{SERVICE_DOMAIN}.microcms.io/api/v1/{ENDPOINT}/{content_id}"
    
    # 送信するデータを構築
    data = {
        'title': article_data.get('title', ''),
    }
    
    # rawContent があれば追加
    if article_data.get('rawContent'):
        data['rawContent'] = article_data['rawContent']
    
    # richContent があれば追加
    if article_data.get('richContent'):
        data['richContent'] = article_data['richContent']
    
    # postDate があれば追加
    if article_data.get('postDate'):
        data['postDate'] = article_data['postDate']
    
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

def publish_article(content_id):
    """記事を公開状態にする"""
    url = f"https://{SERVICE_DOMAIN}.microcms.io/api/v1/{ENDPOINT}/{content_id}/status"
    
    data = json.dumps({'status': ['PUBLISH']}).encode('utf-8')
    
    req = urllib.request.Request(url, data=data, headers={
        'X-MICROCMS-API-KEY': API_KEY,
        'Content-Type': 'application/json'
    }, method='PATCH')
    
    try:
        with urllib.request.urlopen(req) as res:
            return True, None
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8')
        return False, f"{e.code}: {error_body}"

def main():
    print("新しいmicroCMSサービスにデータをインポートしています...")
    print(f"サービス: {SERVICE_DOMAIN}")
    print(f"エンドポイント: {ENDPOINT}")
    print()
    
    # JSONからデータを読み込む
    try:
        with open('export_data.json', 'r', encoding='utf-8') as f:
            articles = json.load(f)
    except FileNotFoundError:
        print("エラー: export_data.json が見つかりません")
        print("先に export_data.py を実行してデータをエクスポートしてください")
        return
    
    print(f"{len(articles)}件の記事をインポートします...")
    print()
    
    success = 0
    failed = 0
    
    for i, article in enumerate(articles):
        # 記事を作成
        ok, error = create_article(article)
        
        if ok:
            # 公開状態にする
            pub_ok, pub_error = publish_article(article['id'])
            if pub_ok:
                success += 1
                print(f"[{i+1}/{len(articles)}] ✓ {article['id']}: {article['title'][:30]}")
            else:
                failed += 1
                print(f"[{i+1}/{len(articles)}] △ {article['id']}: 作成OK、公開失敗 - {pub_error}")
        else:
            failed += 1
            print(f"[{i+1}/{len(articles)}] ✗ {article['id']}: {error}")
        
        # API制限を避けるため少し待機
        time.sleep(0.3)
    
    print(f"\n完了: 成功 {success}件 / 失敗 {failed}件")

if __name__ == '__main__':
    main()
