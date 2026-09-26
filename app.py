from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import re

app = FastAPI()

def clean_html(text):
    text = re.sub(r'<script.*?</script>', '', text, flags=re.DOTALL)
    text = re.sub(r'<style.*?</style>', '', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()[:5000]

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <body style="background:#0a0a0a;color:#00ff88;font-family:monospace;padding:40px;text-align:center">
    <h1 style="font-size:40px">ZQXLO LIVE - Phase 1 - 5 Sources ACTIVE!</h1>
    <p>Wikipedia + DuckDuckGo + Wiki-Summary + YouTube + WEBSITE READER</p>
    <p>TASK 3 - Website Reader LIVE!</p>
    <br>
    <a href="/search?q=Elon" style="color:#00ff88;border:1px solid #00ff88;padding:10px 20px;text-decoration:none;margin:10px">Test /search?q=Elon</a>
    <a href="/read?url=https://en.wikipedia.org/wiki/Elon_Musk" style="color:#00aaff;border:1px solid #00aaff;padding:10px 20px;text-decoration:none;margin:10px">Test /read?url=Wiki</a>
    </body>
    """

@app.get("/search")
def search(q: str):
    results = []
    try:
        # Wikipedia
        r = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={q}&format=json", timeout=5).json()
        for item in r.get("query", {}).get("search", [])[:3]:
            results.append({"title": item["title"], "link": f"https://en.wikipedia.org/wiki/{item['title'].replace(' ','_')}", "snippet": clean_html(item["snippet"])[:200], "source": "wikipedia"})
    except: pass
    try:
        # DuckDuckGo
        r = requests.get(f"https://api.duckduckgo.com/?q={q}&format=json", timeout=5).json()
        if r.get("AbstractText"):
            results.append({"title": r.get("Heading", q), "link": r.get("AbstractURL", ""), "snippet": r.get("AbstractText", "")[:200], "source": "duckduckgo"})
    except: pass
    try:
        # YouTube
        results.append({"title": f"{q} - YouTube", "link": f"https://www.youtube.com/results?search_query={q}", "snippet": f"Watch {q} videos", "source": "youtube"})
    except: pass

    return {"query": q, "count": len(results), "engine": "ZQXLO Phase-1 | 4 Sources", "results": results}

@app.get("/read")
def read_url(url: str):
    try:
        headers = {"User-Agent": "Mozilla/5.0 ZQXLO Bot"}
        r = requests.get(url, headers=headers, timeout=10)
        text = clean_html(r.text)
        return {"url": url, "length": len(text), "engine": "ZQXLO Website Reader", "content": text[:4000]}
    except Exception as e:
        return {"url": url, "error": str(e)}
