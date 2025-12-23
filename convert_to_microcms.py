#!/usr/bin/env python3
"""
WordPress CSVからmicroCMS用CSVへの変換スクリプト
"""
import csv
import re

INPUT_FILE = 'wp_posts_utf8.csv'
OUTPUT_FILE = 'microcms_import.csv'

def clean_html(html_content):
    if not html_content:
        return ''
    content = html_content.strip()
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content

def generate_id(post_id):
    return f"post{post_id}"

def main():
    articles = []
    
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    lines = content.replace('\r\n', '\n').replace('\r', '\n').split('\n')
    current_record = []
    
    for line in lines:
        if re.match(r'^"\d+","', line):
            if current_record:
                full_record = '\n'.join(current_record)
                match = re.match(r'"(\d+)","([^"]*?)","(.*?)","(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"', full_record, re.DOTALL)
                if match:
                    post_id, title, body, _ = match.groups()
                    if title.strip():
                        articles.append({
                            'id': generate_id(post_id),
                            'title': title.strip(),
                            'content': clean_html(body)
                        })
            current_record = [line]
        elif current_record:
            current_record.append(line)
    
    if current_record:
        full_record = '\n'.join(current_record)
        match = re.match(r'"(\d+)","([^"]*?)","(.*?)","(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"', full_record, re.DOTALL)
        if match:
            post_id, title, body, _ = match.groups()
            if title.strip():
                articles.append({
                    'id': generate_id(post_id),
                    'title': title.strip(),
                    'content': clean_html(body)
                })
    
    # microCMS用CSV出力（id, title, contentのみ）
    with open(OUTPUT_FILE, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_ALL)
        writer.writerow(['id', 'title', 'content'])
        for article in articles:
            writer.writerow([article['id'], article['title'], article['content']])
    
    print(f'変換完了: {len(articles)}件')

if __name__ == '__main__':
    main()
