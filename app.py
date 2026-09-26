from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests
import re

app = FastAPI()

def clean(text):
    text = re.sub(r'<[^>]+>', ' ', text)
    return re.sub(r'\s+', ' ', text).strip()

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ZQXLO - AI Search</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:'Segoe UI',monospace}
body{background:#080808;color:#fff;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.header{margin-top:60px;text-align:center}
.logo{font-size:60px;font-weight:900;letter-spacing:6px;color:#00ff88;text-shadow:0 0 20px #00ff8866}
.sub{color:#888;margin-top:10px;font-size:14px;letter-spacing:2px}
.search-box{margin-top:40px;width:90%;max-width:650px;display:flex;gap:10px;background:#141414;border:1px solid #222;border-radius:12px;padding:8px}
.search-box input{flex:1;background:transparent;border:none;color:#fff;font-size:18px;padding:12px;outline:none}
.search-box button{background:#00ff88;color:#000;border:none;padding:12px 22px;border-radius:8px;font-weight:800;cursor:pointer}
.tabs{margin-top:20px;display:flex;gap:12px}
.tab{padding:8px 16px;border-radius:20px;border:1px solid #222;background:#111;color:#888;cursor:pointer;font-size:13px}
.tab.active{border-color:#00ff88;color:#00ff88;background:#00ff8815}
.results{margin-top:30px;width:90%;max-width:700px;padding-bottom:60px}
.card{background:#121212;border:1px solid #1e1e1e;border-radius:12px;padding:18px;margin-bottom:14px}
.card.src{font-size:11px;color:#00ff88;text-transform:uppercase;letter-spacing:1px}
.card.title{font-size:18px;margin:8px 0}
.card.title a{color:#fff;text-decoration:none}
.card.snippet{color:#999;font-size:14px;line-height:1.5}
.loader{display:none;text-align:center;color:#00ff88;margin-top:30px}
.footer{margin-top:auto;padding:20px;color:#333;font-size:12px}
</style>
</head>
<body>
<div class="header"><div class="logo">ZQXLO</div><div class="sub">PHASE-1 • 5 SOURCES • LIVE ON ULTIMUS</div></div>
<div class="tabs">
<div class="tab active" onclick="setMode('search')" id="t-search">🔍 Web Search</div>
<div class="tab" onclick="setMode('read')" id="t-read">🌐 Read Website</div>
</div>
<div class="search-box">
<input id="q" placeholder="Ask anything... e.g. Elon Musk" onkeydown="if(event.key==='Enter') doSearch()">
<button onclick="doSearch()">GO</button>
</div>
<div class="loader" id="loader">⚡ ZQXLO Searching...</div>
<div class="results" id="results"></div>
<div class="footer">Built by you on ULTIMUS • zqxlo.onrender.com</div>
<script>
let mode='search';
function setMode(m){
 mode=m;
 document.querySelectorAll('.tab').forEach(t=>t.classList.remove('active'));
 document.getElementById('t-'+m).classList.add('active');
 document.getElementById('q').placeholder = m==='search'? 'Ask anything... e.g. Elon Musk' : 'Paste any URL... e.g. https://en.wikipedia.org/wiki/AI';
 document.getElementById('results').innerHTML='';
}
async function doSearch(){
 let query=document.getElementById('q').value.trim();
 if(!query) return;
 let resDiv=document.getElementById('results');
 let loader=document.getElementById('loader');
 loader.style.display='block'; resDiv.innerHTML='';
 try{
   let url = mode==='search'? `/search?q=${encodeURIComponent(query)}` : `/read?url=${encodeURIComponent(query)}`;
   let r= await fetch(url); let data= await r.json();
   loader.style.display='none';
   if(mode==='search'){
     resDiv.innerHTML=data.results.map(x=>`<div class=card><div class=src>${x.source}</div><div class=title><a href="${x.link}" target="_blank">${x.title}</a></div><div class=snippet>${x.snippet||''}</div></div>`).join('');
   }else{
     resDiv.innerHTML=`<div class=card><div class=src>WEBSITE READER • ${data.length} chars</div><div class=title>${data.url}</div><div class=snippet style="white-space:pre-wrap;color:#ccc">${(data.content||'').substring(0,4000)}</div></div>`;
   }
 }catch(e){ loader.style.display='none'; resDiv.innerHTML='<div class=card>Error: '+e.message+'</div>';}
}
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def home():
    return HTML_PAGE

@app.get("/search")
def search(q: str):
    results = []
    # 1. Wikipedia search
    try:
        r = requests.get(f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={q}&format=json&srlimit=3", headers={"User-Agent":"ZQXLO/1.0"}, timeout=8).json()
        for item in r.get("query", {}).get("search", []):
            results.append({"title": item["title"], "link": f"https://en.wikipedia.org/wiki/{item['title'].replace(' ','_')}", "snippet": clean(item["snippet"])[:250], "source": "wikipedia"})
    except Exception as e:
        print("wiki search fail", e)
    # 2. Wikipedia summary
    try:
        r = requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{q.replace(' ','_')}", headers={"User-Agent":"ZQXLO/1.0"}, timeout=8).json()
        if r.get("extract"):
            results.append({"title": r.get("title", q), "link": r.get("content_urls",{}).get("desktop",{}).get("page",""), "snippet": r.get("extract","")[:300], "source": "wiki-summary"})
    except: pass
    # 3. DuckDuckGo
    try:
        r = requests.get(f"https://api.duckduckgo.com/?q={q}&format=json&pretty=1", headers={"User-Agent":"ZQXLO/1.0"}, timeout=8).json()
        if r.get("AbstractText"):
            results.append({"title": r.get("Heading") or q, "link": r.get("AbstractURL",""), "snippet": r.get("AbstractText","")[:300], "source": "duckduckgo"})
        for topic in r.get("RelatedTopics", [])[:2]:
            if isinstance(topic, dict) and topic.get("Text"):
                results.append({"title": topic.get("Text","").split(" - ")[0][:60], "link": topic.get("FirstURL",""), "snippet": topic.get("Text","")[:250], "source": "duckduckgo"})
    except: pass
    # 4. YouTube (always works)
    results.append({"title": f"{q} - Videos", "link": f"https://www.youtube.com/results?search_query={q}", "snippet": f"Watch latest videos, interviews and explainers for {q} on YouTube", "source": "youtube"})
    results.append({"title": f"{q} - News & Articles", "link": f"https://www.google.com/search?q={q}", "snippet": f"Latest news, articles and official sites about {q}", "source": "google-search"})

    if len(results)==0:
        results.append({"title": "No results, try Google", "link": f"https://www.google.com/search?q={q}", "snippet": "Fallback link", "source": "fallback"})

    return {"query": q, "count": len(results), "engine": "ZQXLO Phase-1 | 5 Sources FIXED", "results": results[:8]}

@app.get("/read")
def read_url(url: str):
    try:
        r = requests.get(url, headers={"User-Agent":"Mozilla/5.0 ZQXLO Bot"}, timeout=10)
        text = re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', r.text, flags=re.DOTALL)
        text = re.sub(r'\s+', ' ', text).strip()
        return {"url": url, "length": len(text), "engine": "ZQXLO Website Reader", "content": text[:5000]}
    except Exception as e:
        return {"url": url, "error": str(e)}
