from flask import Flask, request, render_template, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import os
import random
import string
from urllib.parse import urljoin, urlparse

app = Flask(__name__)

# 保存ディレクトリ
SAVE_DIR = 'saved_pages'

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def download_image(url, save_dir):
    try:
        response = requests.get(url)
        response.raise_for_status()
        filename = os.path.basename(urlparse(url).path)
        file_path = os.path.join(save_dir, filename)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        return filename
    except requests.exceptions.RequestException:
        return None

def fix_links_and_download_images(soup, base_url, save_dir):
    for tag in soup.find_all(['a', 'img', 'link', 'script']):
        if tag.name == 'a' and tag.get('href'):
            tag['href'] = urljoin(base_url, tag['href'])
        elif tag.name in ['img', 'script'] and tag.get('src'):
            img_url = urljoin(base_url, tag['src'])
            filename = download_image(img_url, save_dir)
            if filename:
                tag['src'] = filename
        elif tag.name == 'link' and tag.get('href'):
            tag['href'] = urljoin(base_url, tag['href'])
    return soup

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proxy', methods=['POST'])
def proxy():
    data = request.get_json()
    url = data.get('url')
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    headers = {
        'Accept-Language': 'ja,en;q=0.9'  # 日本語を優先し、次に英語を指定
    }

    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
    except requests.exceptions.RequestException:
        return jsonify({'url': url, 'title': 'No Title', 'https_failed': True})

    soup = BeautifulSoup(resp.content, 'html.parser')
    title = soup.title.string if soup.title else 'No Title'

    # リンクと画像のURLを修正し、画像をダウンロード
    soup = fix_links_and_download_images(soup, url, SAVE_DIR)

    # 保存
    random_string = generate_random_string()
    file_path = os.path.join(SAVE_DIR, random_string + '.html')
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    return jsonify({'url': url, 'title': title, 'https_failed': False, 'saved_path': f'/m4a1/{random_string}'})

@app.route('/m4a1/<path:filename>')
def serve_saved_page(filename):
    return send_from_directory(SAVE_DIR, filename + '.html')

if __name__ == '__main__':
    app.run(debug=True)
