from flask import Flask, request, jsonify
import requests
app = Flask(__name__)
HEADERS = {'User-Agent': 'ZQXLO/1.0 (ktix-studio phase-1)'}

@app.route('/')
def home():
    return '<h1>ZQXLO LIVE - Phase 1</h1><p>Engine OK - Multi-Source</p><p>Try /search?q=AI</p><p>Sources: Wikipedia + DuckDuckGo</p>'

@app.route('/search')
def search():
    q = request.args.get('q','').strip()
    if not q:
        return jsonify({"error": "Add?q=your query"})

    all_results = []

    # SOURCE 1: Wikipedia
    try:
        wiki_url = f'https://en.wikipedia.org/w/api.php?action=opensearch&search={q}&limit=5&format=json'
        r = requests.get(wiki_url, headers=HEADERS, timeout=10)
        data = r.json()
        for i, title in enumerate(data[1]):
            all_results.append({
                "source": "wikipedia",
                "title": title,
                "link": data[3][i] if i < len(data[3]) else "",
                "snippet": data[2][i] if i < len(data[2]) else ""
            })
    except Exception as e:
        print("Wiki fail", e)

    # SOURCE 2: DuckDuckGo Instant Answer
    try:
        ddg_url = f'https://api.duckduckgo.com/?q={q}&format=json&pretty=1'
        r = requests.get(ddg_url, headers=HEADERS, timeout=10)
        ddg = r.json()
        if ddg.get('AbstractText'):
            all_results.append({
                "source": "duckduckgo",
                "title": ddg.get('Heading') or f"{q} - Info",
                "link": ddg.get('AbstractURL') or f"https://duckduckgo.com/?q={q}",
                "snippet": ddg.get('AbstractText')[:200]
            })
        # Related topics also
        for topic in ddg.get('RelatedTopics', [])[:3]:
            if isinstance(topic, dict) and 'Text' in topic:
                all_results.append({
                    "source": "duckduckgo",
                    "title": topic.get('Text','').split(' - ')[0][:60],
                    "link": topic.get('FirstURL',''),
                    "snippet": topic.get('Text','')[:150]
                })
    except Exception as e:
        print("DDG fail", e)

    # If still empty, fallback
    if not all_results:
        all_results.append({
            "source": "zqxlo-fallback",
            "title": f"Search {q}",
            "link": f"https://duckduckgo.com/?q={q}",
            "snippet": f"ZQXLO Phase 1 - Try DuckDuckGo for {q}"
        })

    return jsonify({
        "engine": "ZQXLO Phase-1 Multi-Source",
        "query": q,
        "count": len(all_results),
        "results": all_results
    })

@app.route('/read')
def read():
    url = request.args.get('url','')
    if not url:
        return jsonify({"error": "Add?url="})
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        return jsonify({"url": url, "preview": r.text[:3000], "length": len(r.text)})
    except Exception as e:
        return jsonify({"error": str(e)[:300]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
