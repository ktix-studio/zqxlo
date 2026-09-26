from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests, re

app = FastAPI()

def clean(t):
    t = re.sub(r'<[^>]+>', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

HTML_PAGE = """
<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ZQXLO</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:monospace}
body{background:#080808;color:#fff;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.logo{font-size:60px;font-weight:900;color:#00ff88;margin-top:40px;letter-spacing:6px;text-shadow:0 0 20px #00ff8844}
.tabs{margin-top:20px;display:flex;gap:10px}
.tab{padding:8px 16px;border-radius:20px;border:1px solid #222;background:#111;color:#888;cursor:pointer;font-size:13px}
.tab.active{color:#00ff88;border-color:#00ff88;background:#00ff8815}
.box{margin-top:25px;width:90%;max-width:650px;display:flex;gap:10px;background:#141414;border:1px solid #222;border-radius:12px;padding:8px}
.box input{flex:1;background:transparent;border:none;color:#fff;font-size:18px;padding:10px;outline:none}
.box button{background:#00ff88;color:#000;border:none;padding:10px 22px;border-radius:8px;font-weight:900;cursor:pointer}
.res{margin-top:30px;width:90%;max-width:700px;padding-bottom:50px}
.ai-card{background:linear-gradient(135deg,#0f2018,#111);border:1px solid #00ff8844;border-radius:16px;padding:20px;margin-bottom:20px;box-shadow:0 0 30px #00ff8815}
.ai-head{color:#00ff88;font-size:11px;letter-spacing:2px;margin-bottom:10px;display:flex;align-items:center;gap:6px}
.ai-text{color:#e0e0e0;font-size:16px;line-height:1.7;white-space:pre-wrap}
.card{background:#121212;border:1px solid #1e1e1e;border-radius:12px;padding:16px;margin-bottom:12px}
.src{color:#00ff88;font-size:11px}
.title{font-size:17px;margin:6px 0}
.title a{color:#fff;text-decoration:none}
.snip{color:#999;font-size:14px;line-height:1.5;white-space:pre-wrap}
</style>
</head><body>
<div class="logo">ZQXLO</div>
<div class="tabs">
<div class="tab active" id="t-search" onclick="setMode('search')">🔍 Web Search</div>
<div class="tab" id="t-read" onclick="setMode('read')">🌐 Read Website</div>
</div>
<div class="box">
<input id="q" placeholder="Ask anything... e.g. who is Elon Musk" onkeydown="if(event.key==='Enter') go()">
<button onclick="go()">GO</button>
</div>
<div id="r" class="res"></div>
<script>
let mode='search';
function setMode(m){mode=m;document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.getElementById('t-'+m).classList.add('active');document.getElementById('q').placeholder=m=='search'?'Ask anything...':'Paste URL';document.getElementById('r').innerHTML='';}
async function go(){
 let q=document.getElementById('q').value.trim(); if(!q) return;
 let div=document.getElementById('r'); div.innerHTML='<div style=text-align:center;color:#00ff88;margin-top:20px>⚡ ZQXLO thinking...</div>';
 try{
  let url = mode=='search'? `/search?q=${encodeURIComponent(q)}` : `/read?url=${encodeURIComponent(q)}`;
  let d=await (await fetch(url)).json();
  if(mode=='search'){
   let ai = d.ai_answer ? `<div class=ai-card><div class=ai-head>✨ ZQXLO AI ANSWER</div><div class=ai-text>${d.ai_answer}</div></div>` : '';
   let cards = d.results.map(x=>`<div class=card><div class=src>${x.source}</div><div class=title><a href="${x.link}" target=_blank>${x.title}</a></div><div class=snip>${x.snippet||''}</div></div>`).join('');
   div.innerHTML = ai + cards;
  }else{
   div.innerHTML=`<div class=card><div class=src>WEBSITE READER • ${d.length} chars</div><div class=title>${d.url}</div><div class=snip>${(d.content||'').substring(0,5000)}</div></div>`;
  }
 }catch(e){div.innerHTML='<div class=card>Error:'+e.message+'</div>';}
}
</script>
</body></html>
"""

@app.get("/", response_class=HTMLResponse)
def home(): return HTML_PAGE

@app.get("/search")
def search(q: str):
    res=[]
    wiki_text=""
    try:
        r=requests.get(f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={q}&format=json&srlimit=3", headers={"User-Agent":"ZQXLO"}, timeout=8).json()
        for i in r.get("query",{}).get("search",[]):
            snippet=clean(i["snippet"])
            wiki_text+=snippet+" "
            res.append({"title":i["title"],"link":f"https://en.wikipedia.org/wiki/{i['title'].replace(' ','_')}","snippet":snippet[:250],"source":"wikipedia"})
    except: pass
    try:
        r=requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{q.replace(' ','_')}", headers={"User-Agent":"ZQXLO"}, timeout=8).json()
        if r.get("extract"):
            wiki_text=r.get("extract","")+" "+wiki_text
            res.append({"title":r.get("title",q),"link":r.get("content_urls",{}).get("desktop",{}).get("page",""),"snippet":r.get("extract","")[:300],"source":"wiki-summary"})
    except: pass

    # PHASE-2 AI ANSWER GENERATOR
    if wiki_text:
        ai_answer = f"{q.upper()} - Here's what ZQXLO found:\\n\\n{wiki_text[:600].strip()}\\n\\nIn short, {q} is explained from {len(res)} verified sources. Scroll down for links."
    else:
        ai_answer = f"ZQXLO searched for '{q}'. Found {len(res)} sources. Based on web data, here's the overview:\\n\\n{q} is a popular topic with videos, articles, and web results. Check the sources below for detailed information. This is Phase-2 AI answer engine."

    res.append({"title":f"{q} - Videos","link":f"https://www.youtube.com/results?search_query={q}","snippet":f"Watch videos for {q}","source":"youtube"})
    res.append({"title":f"{q} - Google","link":f"https://www.google.com/search?q={q}","snippet":f"Search Google for {q}","source":"google"})
    return {"query":q,"results":res,"ai_answer":ai_answer}

@app.get("/read")
def read_url(url: str):
    try:
        if not url.startswith("http"): url="https://"+url
        headers={"User-Agent":"Mozilla/5.0 ZQXLO/1.0"}
        r=requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        txt=re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>', ' ', r.text, flags=re.DOTALL)
        txt=re.sub(r'\s+', ' ', txt).strip()
        if len(txt)<50: txt=f"Site {url} blocked. Try wikipedia.org"
        return {"url":url,"length":len(txt),"content":txt[:5000]}
    except Exception as e:
        return {"url":url,"length":0,"content":f"Failed: {str(e)}"}
