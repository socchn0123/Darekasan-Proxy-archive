from flask import Flask, request, render_template, jsonify, send_from_directory
import requests
from bs4 import BeautifulSoup
import os
import random
import string

app = Flask(__name__)

# 保存ディレクトリ
SAVE_DIR = 'saved_pages'

if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

def generate_random_string(length=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/proxy', methods=['POST'])
def proxy():
    data = request.get_json()
    url = data.get('url')
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'https://' + url

    try:
        resp = requests.get(url)
        resp.raise_for_status()
    except requests.exceptions.RequestException:
        return jsonify({'url': url, 'title': 'No Title', 'https_failed': True})

    soup = BeautifulSoup(resp.content, 'html.parser')
    title = soup.title.string if soup.title else 'No Title'

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
