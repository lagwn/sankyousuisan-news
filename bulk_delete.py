#!/usr/bin/env python3
"""
microCMS 一括削除スクリプト
全記事を削除します（CSVインポート前に使用）
"""
import urllib.request
import urllib.error
import json
import time

SERVICE_DOMAIN = 'sankyou-suisan'
API_KEY = 'u3OWoP9egHtQhAmWO6KlNbNB2xzbPkSTH4hd'
ENDPOINT = 'news'

def get_all_content_ids():
    """全記事のIDを取得"""
    all_ids = []
    offset = 0
    limit = 100
    
    while True:
        url = f"https://{SERVICE_DOMAIN}.microcms.io/api/v1/{ENDPOINT}?limit={limit}&offset={offset}&fields=id"
        req = urllib.request.Request(url, headers={'X-MICROCMS-API-KEY': API_KEY})
        
        try:
            with urllib.request.urlopen(req) as res:
                data = json.loads(res.read().decode('utf-8'))
                contents = data.get('contents', [])
                all_ids.extend([c['id'] for c in contents])
                print(f"  取得中... {len(all_ids)}件")
                if len(contents) < limit:
                    break
                offset += limit
        except urllib.error.HTTPError as e:
            print(f"取得エラー: {e.code}")
            break
    
    return all_ids

def delete_article(content_id):
    """記事を削除"""
    url = f"https://{SERVICE_DOMAIN}.microcms.io/api/v1/{ENDPOINT}/{content_id}"
    
    req = urllib.request.Request(url, headers={
        'X-MICROCMS-API-KEY': API_KEY
    }, method='DELETE')
    
    try:
        with urllib.request.urlopen(req) as res:
            return True
    except urllib.error.HTTPError as e:
        print(f"  削除エラー: {content_id} - {e.code}")
        return False

def main():
    print("記事IDを取得中...")
    content_ids = get_all_content_ids()
    
    if not content_ids:
        print("削除する記事がありません")
        return
    
    print(f"\n{len(content_ids)}件の記事を削除します...")
    print("削除中...")
    success = 0
    for i, content_id in enumerate(content_ids):
        if delete_article(content_id):
            success += 1
            print(f"[{i+1}/{len(content_ids)}] 削除: {content_id}")
        time.sleep(0.3)  # API制限を避けるため
    
    print(f"\n完了: {success}/{len(content_ids)}件を削除しました")
    print("CSVインポートを実行してください。")

if __name__ == '__main__':
    main()
