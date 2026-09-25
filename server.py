from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
HEADERS = {'User-Agent': 'ZQXLO/1.0'}

@app.route('/')
def home():
    return '<h1>ZQXLO LIVE - Phase 1</h1><p>Engine OK - Frontend building...</p><p>Try /search?q=AI</p>'

@app.route('/search')
def search():
    q = request.args.get('q','')
    try:
        r = requests.get(f'https://en.wikipedia.org/w/api.php?action=opensearch&search={q}&limit=5&format=json', headers=HEADERS, timeout=15)
        data = r.json()
        results = [{"title":t} for t in data[1]]
        return jsonify({"query":q,"results":results})
    except Exception as e:
        return jsonify({"query":q,"error":str(e)[:200]})

@app.route('/read')
def read():
    url = request.args.get('url','')
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        return jsonify({"preview":r.text[:2000]})
    except Exception as e:
        return jsonify({"error":str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
