from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <h1>ZQXLO ⚡ LIVE V2</h1>
    <p>AI that connects to everything</p>
    <p>Built by ktix-studio</p>
    <p>Try: /search?q=What is AI? | /read?url=https://example.com</p>
    '''

@app.route('/search')
def search():
    q = request.args.get('q', '')
    try:
        # Use Wikipedia - never blocked on Render
        r = requests.get(f'https://en.wikipedia.org/w/api.php?action=opensearch&search={q}&limit=5&format=json', timeout=15)
        data = r.json()
        results = [f"{title}: https://en.wikipedia.org/wiki/{title.replace(' ', '_')}" for title in data[1]]
        return jsonify({"engine": "ZQXLO V2 Wiki", "query": q, "result": results if results else "No results, but ZQXLO is LIVE!"})
    except Exception as e:
        return jsonify({"engine": "ZQXLO V2", "query": q, "result": f"ZQXLO LIVE! Query received: {q}. Error: {str(e)[:100]}"})

@app.route('/read')
def read():
    url = request.args.get('url', '')
    try:
        r = requests.get(url, timeout=15, headers={'User-Agent': 'ZQXLO-Bot/1.0'})
        return jsonify({"url": url, "content": r.text[:2000]})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
