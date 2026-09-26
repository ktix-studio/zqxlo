from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import requests, re
app=FastAPI()
def clean(t):
    import re
    t=re.sub(r'<[^>]+>',' ',t)
    return re.sub(r'\s+',' ',t).strip()

HTML_PAGE = """
<!DOCTYPE html><html><head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ZQXLO</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family:monospace}
body{background:#080808;color:#fff;min-height:100vh;display:flex;flex-direction:column;align-items:center}
.header{width:100%;display:flex;align-items:center;justify-content:space-between;padding:14px 18px}
.hamburger{font-size:22px;color:#888;cursor:pointer;padding:8px}
.logo{font-size:38px;font-weight:900;color:#00ff88;letter-spacing:5px;text-shadow:0 0 20px #00ff8844}
.right-icons{display:flex;gap:14px;color:#666;font-size:18px}
.sidebar{position:fixed;left:-280px;top:0;width:260px;height:100%;background:#101010;border-right:1px solid #222;transition:0.3s;z-index:99;padding:20px}
.sidebar.open{left:0}
.sidebar h3{color:#00ff88;margin-bottom:20px}
.sidebar a{display:block;color:#999;padding:10px 0;text-decoration:none;font-size:14px;border-bottom:1px solid #1a1a1a}
.overlay{display:none;position:fixed;top:0;left:0;width:100%;height:100%;background:#0008;z-index:98}
.overlay.show{display:block}
.tabs{margin-top:10px;display:flex;gap:10px}
.tab{padding:8px 16px;border-radius:20px;border:1px solid #222;background:#111;color:#888;cursor:pointer;font-size:12px}
.tab.active{color:#00ff88;border-color:#00ff88;background:#00ff8815}
.search-wrap{margin-top:22px;width:90%;max-width:680px;display:flex;align-items:center;gap:8px;background:#141414;border:1px solid #222;border-radius:14px;padding:8px 10px}
.plus{width:36px;height:36px;border-radius:50%;background:#1e1e1e;border:1px solid #2a2a2a;color:#00ff88;display:flex;align-items:center;justify-content:center;cursor:pointer;font-size:16px}
.search-wrap input{flex:1;background:transparent;border:none;color:#fff;font-size:17px;padding:10px;outline:none}
.go{background:#00ff88;color:#000;border:none;padding:10px 20px;border-radius:8px;font-weight:900;cursor:pointer}
.func-menu{position:absolute;bottom:70px;left:5%;background:#151515;border:1px solid #222;border-radius:12px;padding:10px;width:200px;display:none;z-index:10}
.func-menu div{padding:10px;color:#bbb;font-size:13px;cursor:pointer;border-radius:6px}
.func-menu div:hover{background:#1e1e1e;color:#00ff88}
.res{margin-top:28px;width:90%;max-width:700px;padding-bottom:80px}
.ai-card{background:linear-gradient(135deg,#0f2018,#111);border:1px solid #00ff8844;border-radius:16px;padding:18px;margin-bottom:18px;position:relative}
.ai-head{color:#00ff88;font-size:10px;letter-spacing:2px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center}
.speak{cursor:pointer;color:#00ff88;font-size:16px;padding:4px 8px;border:1px solid #00ff8844;border-radius:20px}
.ai-text{color:#e0e0e0;font-size:15px;line-height:1.7}
.card{background:#121212;border:1px solid #1e1e1e;border-radius:12px;padding:14px;margin-bottom:10px}
.src{color:#00ff88;font-size:10px}.title{font-size:16px;margin:5px 0}.title a{color:#fff;text-decoration:none}.snip{color:#999;font-size:13px;line-height:1.5}
</style>
</head><body>
<div class="header">
<div class="hamburger" onclick="toggleMenu()"><i class="fa-solid fa-bars"></i></div>
<div class="logo">ZQXLO</div>
<div class="right-icons"><i class="fa-solid fa-plus"></i></div>
</div>

<div class="sidebar" id="sidebar">
<h3>ZQXLO</h3>
<a href="#" onclick="newChat()"><i class="fa-solid fa-plus"></i> New Search</a>
<a href="#"><i class="fa-solid fa-clock-rotate-left"></i> History</a>
<a href="#" onclick="setMode('read')"><i class="fa-solid fa-globe"></i> Read Website</a>
<a href="#"><i class="fa-solid fa-circle-info"></i> About KTIX Studio</a>
<a href="#"><i class="fa-solid fa-gear"></i> Settings</a>
</div>
<div class="overlay" id="overlay" onclick="toggleMenu()"></div>

<div class="tabs">
<div class="tab active" id="t-search" onclick="setMode('search')">🔍 Web Search</div>
<div class="tab" id="t-read" onclick="setMode('read')">🌐 Read Website</div>
</div>

<div style="position:relative;width:90%;max-width:680px">
<div class="search-wrap">
<div class="plus" onclick="toggleFunc()"><i class="fa-solid fa-plus"></i></div>
<input id="q" placeholder="Ask anything... e.g. what is biology" onkeydown="if(event.key==='Enter') go()">
<button class="go" onclick="go()">GO</button>
</div>
<div class="func-menu" id="funcMenu">
<div onclick="newChat()"><i class="fa-solid fa-broom"></i> Clear / New</div>
<div onclick="copyAnswer()"><i class="fa-solid fa-copy"></i> Copy AI Answer</div>
<div onclick="speakLast()"><i class="fa-solid fa-volume-high"></i> Speak Answer</div>
<div onclick="setMode('read')"><i class="fa-solid fa-link"></i> Read Website</div>
</div>
</div>

<div id="r" class="res"></div>

<script>
let mode='search', lastAnswer='';
function toggleMenu(){document.getElementById('sidebar').classList.toggle('open');document.getElementById('overlay').classList.toggle('show');}
function toggleFunc(){let m=document.getElementById('funcMenu');m.style.display=m.style.display=='block'?'none':'block';}
function newChat(){document.getElementById('q').value='';document.getElementById('r').innerHTML='';toggleFunc();document.getElementById('funcMenu').style.display='none';}
function setMode(m){mode=m;document.querySelectorAll('.tab').forEach(x=>x.classList.remove('active'));document.getElementById('t-'+m).classList.add('active');document.getElementById('q').placeholder=m=='search'?'Ask anything...':'Paste URL e.g. wikipedia.org/wiki/Dog';document.getElementById('r').innerHTML='';document.getElementById('funcMenu').style.display='none';}
function copyAnswer(){if(!lastAnswer)return alert('No answer yet');navigator.clipboard.writeText(lastAnswer);alert('Copied!');}
function speakText(t){if(!t)return;let u=new SpeechSynthesisUtterance(t);u.lang='en-US';speechSynthesis.cancel();speechSynthesis.speak(u);}
function speakLast(){speakText(lastAnswer);}
async function go(){
 let q=document.getElementById('q').value.trim(); if(!q)return;
 let div=document.getElementById('r'); div.innerHTML='<div style=text-align:center;color:#00ff88;margin-top:20px>⚡ ZQXLO thinking...</div>';
 try{
  let url=mode=='search'?`/search?q=${encodeURIComponent(q)}`:`/read?url=${encodeURIComponent(q)}`;
  let d=await (await fetch(url)).json();
  if(mode=='search'){
   lastAnswer=d.ai_answer||'';
   let ai=d.ai_answer?`<div class=ai-card><div class=ai-head><span>✨ ZQXLO AI ANSWER</span><span class=speak onclick="speakLast()"><i class="fa-solid fa-volume-high"></i></span></div><div class=ai-text>${d.ai_answer}</div></div>`:'';
   let cards=d.results.map(x=>`<div class=card><div class=src>${x.source}</div><div class=title><a href="${x.link}" target=_blank>${x.title}</a></div><div class=snip>${x.snippet||''}</div></div>`).join('');
   div.innerHTML=ai+cards;
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
def search(q:str):
    res=[]; wiki_text=""
    try:
        r=requests.get(f"https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch={q}&format=json&srlimit=3", headers={"User-Agent":"ZQXLO"}, timeout=8).json()
        for i in r.get("query",{}).get("search",[]):
            s=clean(i["snippet"]); wiki_text+=s+" "; res.append({"title":i["title"],"link":f"https://en.wikipedia.org/wiki/{i['title'].replace(' ','_')}","snippet":s[:250],"source":"wikipedia"})
    except: pass
    try:
        r=requests.get(f"https://en.wikipedia.org/api/rest_v1/page/summary/{q.replace(' ','_')}", headers={"User-Agent":"ZQXLO"}, timeout=8).json()
        if r.get("extract"): wiki_text=r.get("extract","")+" "+wiki_text; res.append({"title":r.get("title",q),"link":r.get("content_urls",{}).get("desktop",{}).get("page",""),"snippet":r.get("extract","")[:300],"source":"wiki-summary"})
    except: pass
    if wiki_text:
        ai=f"{wiki_text[:650].strip()} In short, {q} explained from {len(res)} verified sources."
    else:
        ai=f"ZQXLO found {len(res)} sources for '{q}'. Check below for details. This is ZQXLO AI answering."
    res.append({"title":f"{q} - Videos","link":f"https://www.youtube.com/results?search_query={q}","snippet":f"Watch {q} videos","source":"youtube"})
    res.append({"title":f"{q} - Google","link":f"https://www.google.com/search?q={q}","snippet":f"Google {q}","source":"google"})
    return {"query":q,"results":res,"ai_answer":ai}
@app.get("/read")
def read_url(url:str):
    try:
        if not url.startswith("http"): url="https://"+url
        r=requests.get(url, headers={"User-Agent":"Mozilla/5.0 ZQXLO"}, timeout=15)
        txt=re.sub(r'<script.*?</script>|<style.*?</style>|<[^>]+>',' ',r.text,flags=re.DOTALL); txt=re.sub(r'\s+',' ',txt).strip()
        return {"url":url,"length":len(txt),"content":txt[:5000]}
    except Exception as e:
        return {"url":url,"length":0,"content":f"Error {e}"}
