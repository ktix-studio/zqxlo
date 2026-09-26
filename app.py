from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
from urllib.parse import quote
import urllib.parse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

def search_wikipedia(q):
    try:
        url = f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={quote(q)}&format=json"
        r = requests.get(url, timeout=5).json()
        results = []
        for item in r.get("query", {}).get("search", [])[:2]:
            results.append({"title": item["title"], "link": f"https://en.wikipedia.org/wiki/{item['title'].replace(' ', '_')}", "snippet": item.get("snippet","")[:150], "source": "wikipedia"})
        return results
    except: return []

def search_duckduckgo(q):
    try:
        url = f"https://api.duckduckgo.com/?q={quote(q)}&format=json&pretty=1"
        r = requests.get(url, timeout=5).json()
        results = []
        for topic in r.get("RelatedTopics", [])[:2]:
            if "Text" in topic and "FirstURL" in topic:
                results.append({"title": topic["Text"][:60], "link": topic["FirstURL"], "snippet": topic["Text"][:150], "source": "duckduckgo"})
        return results
    except: return []

def search_wiki_summary(q):
    try:
        url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{quote(q)}"
        r = requests.get(url, timeout=5).json()
        if "title" in r and "extract" in r:
            return [{"title": r["title"], "link": r.get("content_urls",{}).get("desktop",{}).get("page",""), "snippet": r["extract"][:200], "source": "wiki-summary"}]
        return []
    except: return []

def search_youtube(q):
    try:
        qq = urllib.parse.quote(q)
        url = f"https://vid.puffyan.us/api/v1/search?q={qq}&type=video"
        r = requests.get(url, timeout=8).json()
        results = []
        for item in r[:2]:
            vid = item.get('videoId','')
            results.append({"title": item.get('title',''), "link": f"https://www.youtube.com/watch?v={vid}", "snippet": f"Channel: {item.get('author','')}", "source": "youtube"})
        return results
    except:
        return [{"title": f"{q} - YouTube videos", "link": f"https://www.youtube.com/results?search_query={q}", "snippet": f"Watch {q} videos on YouTube", "source": "youtube"}]

@app.get("/", response_class=HTMLResponse)
def home():
    return """
    <html><body style="font-family: Arial; padding: 20px;">
    <h1>ZQXLO LIVE - Phase 1 - 4 Sources ACTIVE!</h1>
    <h2>Wikipedia + DuckDuckGo + Wiki-Summary + YouTube</h2>
    <p style="color:green; font-size:20px;">TASK 2 DONE - 4 Sources Live!</p>
    <a href="/search?q=Elon">Test Search Elon with YouTube</a>
    </body></html>
    """

@app.get("/search")
def search(q: str = Query(...)):
    all_results = []
    all_results += search_wikipedia(q)
    all_results += search_duckduckgo(q)
    all_results += search_wiki_summary(q)
    all_results += search_youtube(q)
    return {"query": q, "count": len(all_results), "engine": "ZQXLO Phase-1 | 4 Sources", "results": all_results[:8]}

@app.get("/read")
def read(url: str):
    try:
        r = requests.get(url, timeout=8, headers={"User-Agent":"Mozilla/5.0"})
        return {"url": url, "content": r.text[:3000], "length": len(r.text)}
    except Exception as e:
        return {"url": url, "error": str(e)} 
