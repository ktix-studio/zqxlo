from flask import Flask, request, jsonify
import requests

app = Flask(__name__)
HEADERS = {'User-Agent': 'ZQXLO/1.0 (ktix-studio)'}

HTML = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>ZQXLO - AI that connects</title>
<style>
*{margin:0;padding:0;box-sizing:border-box;font-family: system-ui, -apple-system, sans-serif;}
body{background:#0a0a0a;color:white;min-height:100vh;display:flex;flex-direction:column;align-items:center;}
nav{width:100%;padding:20px 30px;display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #222;}
.logo{font-weight:900;font-size:22px;letter-spacing:2px;}.logo span{color:#7c3aed;}
.badge{border:1px solid #333;padding:6px 12px;border-radius:20px;font-size:12px;color:#888;}
.hero{margin-top:80px;text-align:center;padding:20px;}
.hero h1{font-size:48px;font-weight:800;line-height:1.1;}.hero h1 span{background: linear-gradient(90deg,#7c3aed,#ec4899);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.hero p{color:#888;margin-top:15px;font-size:18px;}
.search-box{margin-top:40px;width:90%;max-width:650px;display:flex;background:#151515;border:1px solid #2a2a2a;border-radius:16px;padding:8px;box-shadow:0 10px 40px rgba(0,0,0,0.5);}
.search-box input{flex:1;background:transparent;border:none;outline:none;color:white;padding:12px 15px;font-size:16px;}
.search-box button{background:white;color:black;border:none;padding:12px 22px;border-radius:10px;font-weight:700;cursor:pointer;}
.results{width:90%;max-width:650px;margin-top:30px;padding-bottom:50px;}
.card{background:#151515;border:1px solid #222;border-radius:12px;padding:16px;margin-bottom:12px;transition:0.2s;}
.card:hover{border-color:#333;transform:translateY(-2px);}
.card a{color:white;text-decoration:none;font-weight:600;font-size:16px;}
.card p{color:#777;font-size:13px;margin-top:6px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.status{color:#22c55e;font-size:13px;margin-top:20px;display:flex;align-items:center;gap:6px;}
.dot{width:8px;height:8px;background:#22c55e;border-radius:50%;box-shadow:0 0 10px #22c55e;animation:pulse 2s infinite;}
@keyframes pulse{0%,100%{opacity:1} 50%{opacity:0.5}}
footer{margin-top:auto;padding:20px;color:#444;font-size:12px;}
</style>
</head>
<body>
<nav><div class="logo">ZQXLO<span>⚡</span></div><div class="badge">PHASE 1 • LIVE</div></nav>
<div class="hero">
<h1>AI that connects<br><span>to everything</span></h1>
<p>Built by ktix-studio • Gauhati</p>
<div class="status"><div class="dot"></div> V4 Engine Online • zqxlo.onrender.com</div>
</div>

<div class="search-box">
<input id="q" placeholder="Try: What is AI? Python, Naruto, ISRO..." onkeydown="if(event.key==='Enter')go()">
<button onclick="go()">Search ⚡</button>
</div>

<div id="results" class="results"></div>

<footer>KTIX Studio © 2026 • Phase 1 - Search Engine Live</footer>

<script>
async function go(){
 let q = document.getElementById('q').value.trim();
 if(!q) return;
 let box = document.getElementById('results');
 box.innerHTML = '<div style="color:#666;text-align:center;padding:30px;">ZQXLO is searching... ⚡</div>';
 try{
  let res = await fetch('/search?q='+encodeURIComponent(q));
  let data = await res.json();
  let html = `<div style="color:#888;font-size:13px;margin-bottom:15px;">Found ${data.count||data.results?.length||0} results for "${data.query}" • ${data.engine}</div>`;
  (data.results||[]).forEach(r=>{
   html+=`<div class="card"><a href="${r.link}" target="_blank">${r.title}</a><p>${r.snippet||r.link}</p></div>`;
  });
  if(!data.results || data.results.length==0){
   html+=`<div class="card"><p>${data.message||data.result||'ZQXLO is live but no results'}</p></div>`;
  }
  box.innerHTML = html;
 }catch(e){
  box.innerHTML = '<div class="card"><p>Error: '+e+'</p></div>';
 }
}
</script>
</body>
</html>
"""

@app.route('/')
def home():
    return HTML

@app.route('/search')
def search():
    q = request.args.get('q','').strip()
    if not q: return jsonify({"engine":"ZQXLO V4","error":"Add q"})
    try:
        url = f'https://en.wikipedia.org/w/api.php?action=opensearch&search={q}&limit=8&format=json'
        r = requests.get(url, headers=HEADERS, timeout=20)
        data = r.json()
        results = []
        for i, title in enumerate(data[1]):
            results.append({"title": title, "link": data[3][i] if i < len(data[3]) else f"https://en.wikipedia.org/wiki/{title}", "snippet": data[2][i] if i < len(data[2]) else ""})
        return jsonify({"engine":"ZQXLO V4 PHASE-1","query":q,"count":len(results),"results":results})
    except Exception as e:
        return jsonify({"engine":"ZQXLO V4","query":q,"results":[{"title":f"{q} - Search","link":f"https://en.wikipedia.org/w/index.php?search={q}","snippet":f"ZQXLO LIVE - Query: {q}"}]})

@app.route('/read')
def read():
    url = request.args.get('url','')
    try:
        r = requests.get(url, headers=HEADERS, timeout=20)
        return jsonify({"url":url,"preview":r.text[:3000]})
    except Exception as e:
        return jsonify({"error":str(e)[:300]})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
