from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
HEADERS = {'User-Agent': 'ZQXLO/1.0'}

@app.route('/')
def home():
    return '<h1>ZQXLO LIVE - Phase 1</h1><p>3 Sources Active</p><p>Wikipedia + DuckDuckGo + Wiki-Summary</p>'

@app.route('/search')
def search():
    q = request.args.get('q','').strip()
    if not q:
        return jsonify({"error": "Add?q=your query"})

    all_results = []

    # SOURCE 1: Wikipedia OpenSearch
    try:
        r = requests.get(f'https://en.wikipedia.org/w/api.php?action=opensearch&search={q}&limit=5&format=json', headers=HEADERS, timeout=10)
        data = r.json()
        for i, title in enumerate(data[1]):
            all_results.append({
                "source": "wikipedia",
                "title": title,
                "link": data[3][i] if i < len(data[3]) else "",
                "snippet": data[2][i] if i < len(data[2]) else ""
            })
    except: pass

    # SOURCE 2: DuckDuckGo
    try:
        r = requests.get(f'https://api.duckduckgo.com/?q={q}&format=json&pretty=1', headers=HEADERS, timeout=10)
        ddg = r.json()
        if ddg.get('AbstractText'):
            all_results.append({
                "source": "duckduckgo",
                "title": ddg.get('Heading') or q,
                "link": ddg.get('AbstractURL') or f"https://duckduckgo.com/?q={q}",
                "snippet": ddg.get('AbstractText')[:250]
            })
    except: pass

    # SOURCE 3: NEW - Wikipedia Summary API (full details)
    try:
        r = requests.get(f'https://en.wikipedia.org/api/rest_v1/page/summary/{q}', headers=HEADERS, timeout=10)
        if r.status_code == 200:
            wiki = r.json()
            if wiki.get('extract'):
                all_results.append({
                    "source": "wiki-summary",
                    "title": wiki.get('title') + " - Summary",
                    "link": wiki.get('content_urls',{}).get('desktop',{}).get('page',''),
                    "snippet": wiki.get('extract')[:300]
                })
    except: pass

    if not all_results:
        all_results.append({
            "source": "fallback",
            "title": f"Search {q} on DuckDuckGo",
            "link": f"https://duckduckgo.com/?q={q}",
            "snippet": f"No result, try DuckDuckGo for {q}"
        })

    return jsonify({
        "engine": "ZQXLO Phase-1 | 3 Sources",
        "query": q,
        "count": len(all_results),
        "results": all_results
    })

@app.route('/read')
def read():
    url = request.args.get('url','')
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        return jsonify({"preview": r.text[:3000]})
    except Exception as e:
        return jsonify({"error": str(e)[:200]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
