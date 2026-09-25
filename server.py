# ZQXLO - Web Server for Render
# Like ktix web studio but for AI

from flask import Flask, request, jsonify
from core import ZQXLO

app = Flask(__name__)
zqx = ZQXLO()

@app.route('/')
def home():
    return """
    <h1>ZQXLO ⚡ LIVE</h1>
    <p>AI that connects to everything</p>
    <p>Built by ktix-studio</p>
    <p>Try: /search?q=What is AI? | /read?url=https://example.com</p>
    """

@app.route('/search')
def search():
    query = request.args.get('q', 'What is AI?')
    result = zqx.search_google(query)
    return jsonify({"query": query, "result": result, "engine": "ZQXLO ⚡"})

@app.route('/read')
def read():
    url = request.args.get('url', 'https://example.com')
    result = zqx.read_url(url)
    return jsonify({"url": url, "result": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
