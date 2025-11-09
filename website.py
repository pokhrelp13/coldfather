# ui.py
from flask import Flask, render_template_string
import json

app = Flask(__name__)

# ---------- Shared data ----------
FOOD_NAMES = [
    "Chicken Breast","Leafy Lettuce","Fresh Salmon","Whole Milk","Greek Yogurt",
    "Cheddar Cheese","Cage-Free Eggs","Strawberries","Baby Spinach","Ground Beef",
    "Pork Loin","Brown Rice","Broccoli Crowns","Carrot Sticks","Cottage Cheese",
    "Sourdough Bread","Tomato Soup","Avocado","Blueberries","Romaine Hearts",
    "Cucumber","Mushrooms","Mozzarella","Butter","Hummus"
]  # 25 total

# Image keywords per food for relevant thumbnails
FOOD_IMG_QUERY = {
    "Chicken Breast": "chicken breast raw",
    "Leafy Lettuce": "leafy lettuce",
    "Fresh Salmon": "fresh salmon fillet",
    "Whole Milk": "milk bottle",
    "Greek Yogurt": "greek yogurt",
    "Cheddar Cheese": "cheddar cheese block",
    "Cage-Free Eggs": "eggs carton",
    "Strawberries": "fresh strawberries",
    "Baby Spinach": "baby spinach leaves",
    "Ground Beef": "ground beef raw",
    "Pork Loin": "pork loin",
    "Brown Rice": "brown rice",
    "Broccoli Crowns": "broccoli crowns",
    "Carrot Sticks": "carrot sticks",
    "Cottage Cheese": "cottage cheese bowl",
    "Sourdough Bread": "sourdough bread loaf",
    "Tomato Soup": "tomato soup bowl",
    "Avocado": "avocado halves",
    "Blueberries": "blueberries",
    "Romaine Hearts": "romaine hearts lettuce",
    "Cucumber": "cucumber",
    "Mushrooms": "white mushrooms",
    "Mozzarella": "mozzarella cheese",
    "Butter": "butter block",
    "Hummus": "hummus bowl"
}

# ---------- HOME ----------
home_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>ColdFather</title>
<style>
  :root{
    --bg:#0b1020; --surface:#0f172a; --paper:#ffffff; --ring:rgba(0,0,0,.12);
    --muted:#8892a6; --ink:#0e1324; --yellow-1:#fde047; --yellow-2:#facc15;
    --blue:#2563eb; --grad-1:#111827; --grad-2:#1f2937; --grid-gap:12px;
  }
  *{box-sizing:border-box}
  body{margin:0;font-family:Inter,system-ui,Segoe UI,Roboto,Arial,sans-serif;background:linear-gradient(160deg,var(--bg) 0%, #0a1330 30%, #0a163c 100%);color:#e5e7eb}
  .hero-wrap{position:relative;padding:24px 12px 10px;background:
      radial-gradient(1200px 400px at 50% -10%, rgba(250,204,21,.12), transparent 60%),
      radial-gradient(900px 280px at 80% 0%, rgba(99,102,241,.10), transparent 60%);}
  .hero{max-width:1350px;margin:0 auto}
  .site-title{margin:0;text-align:center;font-size:30px;font-weight:900;letter-spacing:.3px;background:linear-gradient(120deg,#c7d2fe 0%,#e0f2fe 35%,#fef9c3 70%,#fde047 100%);-webkit-background-clip:text;background-clip:text;color:transparent;filter:drop-shadow(0 2px 6px rgba(0,0,0,.35));animation:coldShimmer 3.5s linear infinite}
  @keyframes coldShimmer{0%{text-shadow:0 0 6px rgba(173,216,230,.25)}50%{text-shadow:0 0 10px rgba(173,216,230,.4)}100%{text-shadow:0 0 6px rgba(173,216,230,.25)}}
  .hero-sub{margin:6px auto 0;max-width:820px;text-align:center;color:#c7d2fe;font-size:14px;line-height:1.55}
  .hero-cta{margin-top:12px;display:flex;justify-content:flex-end;gap:8px}
  .btn{border:none;font-weight:800;cursor:pointer;padding:10px 16px;border-radius:999px;font-size:14px}
  #team-btn{background:transparent;border:1px dashed rgba(255,255,255,.22);color:#e5e7eb}
  #login-btn{background:linear-gradient(90deg,var(--yellow-1),var(--yellow-2));color:#0b1020}
  .stats-band{margin:14px auto 6px;max-width:1350px;padding:0 12px;display:grid;grid-template-columns:repeat(4,1fr);gap:12px}
  .stat{background:linear-gradient(180deg,var(--grad-1),var(--grad-2));border:1px solid rgba(255,255,255,.08);color:#e5e7eb;border-radius:14px;padding:10px;text-align:center;box-shadow:inset 0 0 1px rgba(255,255,255,.08),0 12px 36px rgba(2,6,23,.35)}
  .stat .num{font-weight:900;font-size:18px}.stat .lbl{font-size:12px;color:#cbd5e1}
  .container{width:100%;max-width:1350px;margin:0 auto;padding:0 12px 16px;display:grid;grid-template-columns:1fr;gap:var(--grid-gap)}
  @media (min-width:960px){
    .container{grid-template-columns:1.08fr .92fr;align-items:start}
    #more-product{grid-column:1} #prototype-section{grid-column:1} #tracker-section{grid-column:1}
    #food-status{grid-column:2;grid-row:1 / span 3}
  }
  .section{background:var(--paper);color:var(--ink);border-radius:16px;padding:18px 18px 12px;box-shadow:0 30px 60px rgba(0,0,0,.25),0 8px 18px rgba(0,0,0,.18)}
  .section h2{margin:0 0 10px;text-align:center;font-size:22px}
  .section p{color:#404b63;line-height:1.62;font-size:16px}
  .features{display:grid;grid-template-columns:repeat(3,1fr);gap:10px;margin-top:10px}
  .feat{background:#f8fafc;border:1px solid #eef2f7;border-radius:14px;padding:12px;text-align:center;box-shadow:0 10px 24px rgba(2,6,23,.06)}
  .feat h4{margin:0 0 4px;font-size:14px}.feat p{margin:0;color:#64748b;font-size:12px}
  .proto-wrap{position:relative;width:100%;border-radius:12px;overflow:hidden;box-shadow:0 12px 30px rgba(0,0,0,.25)}
  .proto-img{width:100%;display:block;object-fit:cover}
  .proto-caption{position:absolute;bottom:0;left:0;right:0;background:rgba(0,0,0,.55);color:#fef9c3;font-weight:800;font-size:16px;text-align:center;padding:8px 0;text-shadow:0 2px 4px rgba(0,0,0,.5)}
  .tracker-title{font-weight:900;margin:0 0 10px;font-size:16px;text-align:center}
  .tracker-row{display:flex;gap:10px;align-items:center;justify-content:center;flex-wrap:wrap}
  .tracker-row input{width:320px;max-width:100%;padding:12px 14px;border:1px solid #d1d5db;border-radius:12px;font-size:14px}
  .tracker-row button{padding:12px 16px;border:none;border-radius:12px;font-weight:900;font-size:14px;cursor:pointer;background:#2563eb;color:#fff;box-shadow:0 10px 20px rgba(37,99,235,.25)}
  .tracker-hint{margin-top:8px;text-align:center;color:#64748b;font-size:12px}
  .safe-status{margin-top:8px;display:flex;align-items:center;justify-content:center;gap:10px;font-weight:900;color:#065f46}
  .safe-dot{width:10px;height:10px;border-radius:999px;background:#10b981;box-shadow:0 0 0 0 rgba(16,185,129,.7);animation:pulse 1.6s infinite}
  .safe-dot.right{animation-delay:.8s}
  @keyframes pulse{0%{box-shadow:0 0 0 0 rgba(16,185,129,.7);opacity:1}50%{opacity:.6}70%{box-shadow:0 0 0 8px rgba(16,185,129,0)}100%{box-shadow:0 0 0 0 rgba(16,185,129,0);opacity:1}}
  .food-cards{display:flex;flex-direction:column;gap:8px;margin-top:10px}
  .food-card{display:flex;gap:10px;align-items:center;background:#f8fafc;border:1px solid #e5e7eb;border-radius:14px;padding:7px 9px;box-shadow:0 10px 24px rgba(2,6,23,.06)}
  .thumb{width:52px;height:52px;border-radius:10px;object-fit:cover;box-shadow:0 6px 12px rgba(0,0,0,.08)}
  .food-meta{flex:1;display:flex;flex-direction:column;gap:2px}
  .food-name{font-weight:800;font-size:13.5px;line-height:1.2;color:#0b1020}
  .food-table{width:auto;border-collapse:collapse;font-size:12px;line-height:1.2}
  .food-table td{padding:1px 8px 1px 0;color:#111827}
  .kpi{display:inline-flex;gap:6px;font-size:11px;color:#64748b}
  .kpi span{padding:2px 8px;border-radius:999px;background:#fff;border:1px solid #e5e7eb}
  .see-all-btn{margin:10px auto 0;display:block;padding:10px 16px;border:none;border-radius:12px;cursor:pointer;background:linear-gradient(90deg,var(--yellow-1),var(--yellow-2));font-weight:900;font-size:13px;color:#0b1020;box-shadow:0 10px 24px rgba(250,204,21,.25)}
  footer{background:#0f172a;color:#e5e7eb;padding:14px 12px;margin:18px 0 0;box-shadow:0 -2px 10px rgba(0,0,0,.25)}
  .footer-bar{max-width:1350px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;gap:12px}
  .footer-left{font-weight:900;font-size:20px;background:linear-gradient(120deg,#c7d2fe,#fde047);-webkit-background-clip:text;background-clip:text;color:transparent;animation:coldShimmer 3.5s linear infinite}
  .footer-middle{font-weight:700;color:#facc15;text-align:center;font-size:14px;flex:1}
  .footer-right img{width:120px;height:auto}

  /* Team modal */
  #team-modal{display:none;position:fixed;inset:0;background:rgba(0,0,0,.6);z-index:1000;
    align-items:center;justify-content:center;padding:20px}
  .team-content{background:#fff;border-radius:16px;max-width:840px;width:100%;padding:22px 22px 18px;color:#0b1020;
    box-shadow:0 20px 60px rgba(0,0,0,.25)}
  .team-members{display:flex;flex-wrap:wrap;gap:18px;justify-content:center;margin-top:12px}
  .team-member{text-align:center;width:160px}
  .team-member img{width:130px;height:130px;border-radius:12px;object-fit:cover;box-shadow:0 6px 18px rgba(0,0,0,.15)}
  .team-role{font-size:12px;color:#475569;margin-top:4px}
</style>
</head>
<body>
<section class="hero-wrap">
  <div class="hero">
    <h1 class="site-title">ColdFather</h1>
    <p class="hero-sub">Real-time food condition monitoring with compact sensors, anomaly alerts, and a clean dashboard designed for kitchens and cold-chain teams.</p>
    <div class="hero-cta">
      <button class="btn" id="team-btn" aria-haspopup="dialog">Meet the Team</button>
      <button class="btn" id="login-btn" onclick="location.href='/login'">Login</button>
    </div>
  </div>
</section>

<div class="stats-band">
  <div class="stat"><div class="num">10+</div><div class="lbl">Active Facilities</div></div>
  <div class="stat"><div class="num">24/7</div><div class="lbl">Live Monitoring</div></div>
  <div class="stat"><div class="num">±0.2°C</div><div class="lbl">Sensor Accuracy</div></div>
  <div class="stat"><div class="num">MakeUC ’25</div><div class="lbl">Project Prototype</div></div>
</div>

<div class="container">
  <section class="section" id="more-product">
    <h2>More About the Product</h2>
    <p id="about-para-1"></p>
    <p id="about-para-2"></p>
    <div class="features">
      <div class="feat"><h4>Edge Alerts</h4><p>On-device thresholds & anomaly detection.</p></div>
      <div class="feat"><h4>Cold-Chain Fit</h4><p>IP65 casing, probe add-on, long battery.</p></div>
      <div class="feat"><h4>Easy Export</h4><p>CSV, webhooks, and role-based sharing.</p></div>
    </div>
  </section>

  <section class="section" id="prototype-section">
    <h2>Internal Prototype</h2>
    <div class="proto-wrap">
      <img src="/static/thumbnail_IMG_1867.jpg" alt="Internal Prototype" class="proto-img"/>
      <div class="proto-caption">Sensor Assembly Preview</div>
    </div>
  </section>

  <section class="section" id="tracker-section" aria-live="polite">
    <h3 class="tracker-title">Track your Packages REAL-TIME Status</h3>
    <div class="tracker-row">
      <input id="truckCode" type="text" placeholder="Enter Truck Code" />
      <button id="trackBtn" type="button">Search</button>
    </div>
    <div class="tracker-hint" id="trackerHint">Enter your truck code and press Search.</div>
    <div class="safe-status"><span class="safe-dot"></span><span>Food is Safe to Consume</span><span class="safe-dot right"></span></div>
  </section>

  <section class="section" id="food-status">
    <h2>Food Status</h2>
    <div id="food-list" class="food-cards" aria-live="polite"></div>
  </section>
</div>

<!-- Meet the Team Modal -->
<div id="team-modal" role="dialog" aria-modal="true" aria-labelledby="team-title">
  <div class="team-content">
    <h2 id="team-title" style="text-align:center;margin:0">Meet the Team</h2>
    <div class="team-members">
  <div class="team-member">
<img src="/static/ALI.jpg" alt="Team Member"/>    
    <div style="font-weight:800;margin-top:6px">ALI</div>
    <div class="team-role">Hardware & Firmware</div>
  </div>
  <div class="team-member">
    <img src="/static/thumbnail_IMG_5325.jpg" alt="Team Member"/>
    <div style="font-weight:800;margin-top:6px">PRABIN</div>
    <div class="team-role">Frontend & UI Design</div>
  </div>
  <div class="team-member">
    <img src="/static/Kritika.jpg" alt="Team Member"/>
    <div style="font-weight:800;margin-top:6px">KRITIKA</div>
    <div class="team-role">Data & Backend</div>
  </div>
  <div class="team-member">
    <img src="/static/Wasel.jpg" alt="Team Member"/>
    <div style="font-weight:800;margin-top:6px">WASEL</div>
    <div class="team-role">Integration & Testing</div>
  </div>
</div>
    <div style="text-align:center;margin-top:16px">
      <button class="btn" onclick="closeTeam()" style="border:1px solid #e5e7eb;background:#fff">Close</button>
    </div>
  </div>
</div>

<footer>
  <div class="footer-bar">
    <div class="footer-left">ColdFather</div>
    <div class="footer-middle">Prototyped as part of MakeUC 2025 Project</div>
    <div class="footer-right"><img src="/static/make_uc.png" alt="MakeUC Logo" style="height:60px;width:auto;object-fit:contain;"/></div>
  </div>
</footer>

<script>
/* product blurbs */
const blurbs=[
  "We designed for kitchens first: glove-friendly buttons, bright indicators, and a magnetic back.",
  "Our nodes log temperature & humidity with on-device anomaly detection so you get alerts before spoilage.",
  "Seamless cold-chain fit: probe add-on, IP65 enclosure, multi-week battery.",
  "Data syncs via Wi-Fi/BLE. Export CSV, set thresholds, invite teammates."
];
const pick=()=>blurbs[Math.floor(Math.random()*blurbs.length)];
document.getElementById('about-para-1').textContent=pick();
document.getElementById('about-para-2').textContent=pick();

/* REAL FOOD NAMES (first 8 shown), then See All → /foods with 25 items */
const FOOD_NAMES = %FOOD_NAMES%;
const FOOD_IMG_QUERY = %FOOD_IMG_QUERY%;

/* Build a relevant, stable thumbnail per food using loremflickr */
function imgFor(name, idx){
  const q = (FOOD_IMG_QUERY[name] || name).replace(/\s+/g, ',');
  return `https://loremflickr.com/160/160/${encodeURIComponent(q)}?lock=${idx+1}`;
}

const foods = FOOD_NAMES.map((name,i)=>({
  name,
  img: imgFor(name, i),
  temp:(Math.random()*8+1).toFixed(1),
  hum: Math.floor(Math.random()*41)+40
}));

const list=document.getElementById('food-list');
foods.forEach((f,i)=>{
  const card=document.createElement('div');card.className='food-card';
  if(i>=8) card.style.display='none';
  card.innerHTML=`<img class="thumb" src="${f.img}" alt="${f.name}">
  <div class="food-meta">
    <div class="food-name">${f.name}</div>
    <table class="food-table">
      <tr><td>Temperature:</td><td>${f.temp}°C</td></tr>
      <tr><td>Humidity:</td><td>${f.hum}%</td></tr>
    </table>
    <div class="kpi"><span>T: ${f.temp}°C</span><span>H: ${f.hum}%</span></div>
  </div>`;
  list.appendChild(card);
});

const seeAll=document.createElement('button');seeAll.className='see-all-btn';seeAll.textContent='See All Foods';
if(list.children.length>=8) list.insertBefore(seeAll, list.children[8]);
seeAll.onclick=()=>location.href='/foods';

/* Tracker: DEMO -> /simulate */
document.getElementById('trackBtn').onclick=()=>{
  const v=document.getElementById('truckCode').value.trim();
  const h=document.getElementById('trackerHint');
  if(v.toUpperCase()==='DEMO'){ location.href='/simulate?code='+encodeURIComponent(v); return; }
  h.textContent = v ? `Tracking "${v}" (demo only).` : 'Please enter a truck code.';
  h.style.color = v ? '#64748b' : '#dc2626';
};

/* Team modal JS */
const teamBtn=document.getElementById('team-btn');
const teamModal=document.getElementById('team-modal');
function closeTeam(){ teamModal.style.display='none'; }
window.closeTeam = closeTeam;
teamBtn.addEventListener('click', ()=>{ teamModal.style.display='flex'; });
teamModal.addEventListener('click', (e)=>{ if(e.target===teamModal) closeTeam(); });
</script>
</body></html>
""".replace("%FOOD_NAMES%", json.dumps(FOOD_NAMES)).replace("%FOOD_IMG_QUERY%", json.dumps(FOOD_IMG_QUERY))

# ---------- /FOODS (25 items) ----------
foods_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>All Foods • ColdFather</title>
<style>
  :root{--bg:#0b1020;--paper:#ffffff;--ink:#0e1324;--ring:rgba(0,0,0,.12)}
  *{box-sizing:border-box}
  body{margin:0;font-family:Inter,system-ui,Segoe UI,Roboto,Arial,sans-serif;background:linear-gradient(160deg,var(--bg) 0%, #0a1330 30%, #0a163c 100%);color:#e5e7eb}
  .wrap{max-width:1200px;margin:0 auto;padding:16px 12px}
  .bar{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}
  .title{font-weight:900;font-size:24px;background:linear-gradient(120deg,#c7d2fe,#fde047);-webkit-background-clip:text;background-clip:text;color:transparent}
  .back{border:none;border-radius:999px;padding:8px 14px;font-weight:800;cursor:pointer;background:linear-gradient(90deg,#fde047,#facc15);color:#111}
  .grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:10px}
  .card{background:var(--paper);color:var(--ink);border-radius:14px;padding:10px;display:flex;gap:10px;align-items:center;box-shadow:0 10px 26px rgba(0,0,0,.25)}
  .thumb{width:60px;height:60px;border-radius:10px;object-fit:cover;box-shadow:0 6px 12px rgba(0,0,0,.08)}
  .meta{flex:1}
  .name{font-weight:900}
  .small{font-size:13px;color:#374151}
  .chip{display:inline-block;margin-top:4px;padding:4px 8px;border-radius:999px;font-size:12px;font-weight:800}
  .st-bad{background:rgba(239,68,68,.2);border:1px solid rgba(239,68,68,.35)}
  .st-warn{background:rgba(245,158,11,.2);border:1px solid rgba(245,158,11,.35)}
  .st-good{background:rgba(34,197,94,.2);border:1px solid rgba(34,197,94,.35)}
</style>
</head>
<body>
<div class="wrap">
  <div class="bar">
    <div class="title">All Foods (25)</div>
    <button class="back" onclick="location.href='/'">← Back</button>
  </div>

  <div id="grid" class="grid"></div>
</div>

<script>
const FOOD_NAMES = %FOOD_NAMES%;
const FOOD_IMG_QUERY = %FOOD_IMG_QUERY%;

function imgFor(name, idx){
  const q = (FOOD_IMG_QUERY[name] || name).replace(/\s+/g, ',');
  return `https://loremflickr.com/160/160/${encodeURIComponent(q)}?lock=${idx+1}`;
}

function classify(t,h){
  if(t>8 || h>80) return {txt:'Spoiled / Unsafe', cls:'st-bad'};
  if(t>=4 || h>=60) return {txt:'Safe to Consume', cls:'st-warn'};
  return {txt:'Good Condition / Fresh', cls:'st-good'};
}

const grid=document.getElementById('grid');
FOOD_NAMES.forEach((name,i)=>{
  const temp=(Math.random()*8+1).toFixed(1);
  const hum =Math.floor(Math.random()*41)+40;
  const st=classify(temp,hum);
  const card=document.createElement('div');card.className='card';
  card.innerHTML = `
    <img class="thumb" src="${imgFor(name,i)}" alt="${name}">
    <div class="meta">
      <div class="name">${name}</div>
      <div class="small">Temperature: <b>${temp}°C</b> &nbsp; • &nbsp; Humidity: <b>${hum}%</b></div>
      <span class="chip ${st.cls}">${st.txt}</span>
    </div>
  `;
  grid.appendChild(card);
});
</script>
</body>
</html>
""".replace("%FOOD_NAMES%", json.dumps(FOOD_NAMES)).replace("%FOOD_IMG_QUERY%", json.dumps(FOOD_IMG_QUERY))

# ---------- /SIMULATE (table-only, real names) ----------
simulate_html = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>Live Simulation • ColdFather</title>
<style>
  :root{--bg:#0b1020;--paper:#ffffff;--ink:#0e1324}
  *{box-sizing:border-box}
  body{margin:0;font-family:Inter,system-ui,Segoe UI,Roboto,Arial,sans-serif;background:linear-gradient(160deg,var(--bg) 0%, #0a1330 30%, #0a163c 100%);color:#e5e7eb}
  .wrap{max-width:1200px;margin:0 auto;padding:16px 12px}
  .bar{display:flex;justify-content:space-between;align-items:center;gap:12px;margin-bottom:10px}
  .title{font-weight:900;font-size:24px;background:linear-gradient(120deg,#c7d2fe,#fde047);-webkit-background-clip:text;background-clip:text;color:transparent}
  .back{border:none;border-radius:999px;padding:8px 14px;font-weight:800;cursor:pointer;background:linear-gradient(90deg,#fde047,#facc15);color:#111}
  .card{background:var(--paper);color:var(--ink);border-radius:16px;padding:16px;box-shadow:0 30px 60px rgba(0,0,0,.25)}
  table{width:100%;border-collapse:separate;border-spacing:0 8px}
  thead th{text-align:left;font-size:14px;padding:8px 10px;color:#111}
  tbody td{background:#f8fafc;border:1px solid #e5e7eb;padding:10px;border-radius:12px;font-size:14px}
  .chip{display:inline-block;padding:6px 10px;border-radius:999px;font-weight:800;color:#111}
  .st-good{background:rgba(34,197,94,.25);border:1px solid rgba(34,197,94,.35)}
  .st-warn{background:rgba(245,158,11,.25);border:1px solid rgba(245,158,11,.35)}
  .st-bad{background:rgba(239,68,68,.25);border:1px solid rgba(239,68,68,.35)}
</style>
</head>
<body>
<div class="wrap">
  <div class="bar">
    <div class="title">Live Package Simulation</div>
    <button class="back" onclick="location.href='/'">← Back</button>
  </div>

  <div class="card">
    <table>
      <thead>
        <tr>
          <th>Food</th><th>Temperature</th><th>Humidity</th><th>Status</th>
        </tr>
      </thead>
      <tbody id="rows"></tbody>
    </table>
  </div>
</div>

<script>
const FOOD_NAMES = %FOOD_NAMES%;
const foods = FOOD_NAMES.slice(0,10).map(n=>({
  name:n,
  temp:+(Math.random()*5+2).toFixed(1),
  hum: Math.floor(Math.random()*21)+50
}));
function classify(t,h){
  if(t>8 || h>80) return {label:'Spoiled / Unsafe', cls:'st-bad'};
  if(t>=4 || h>=60) return {label:'Safe to Consume', cls:'st-warn'};
  return {label:'Good Condition / Fresh', cls:'st-good'};
}
function ensureUnsafe(){
  const anyBad = foods.some(f=>f.temp>8 || f.hum>80);
  if(!anyBad){
    const i = Math.floor(Math.random()*foods.length);
    Math.random()<0.5 ? (foods[i].temp = +(9 + Math.random()*3).toFixed(1))
                      : (foods[i].hum  = 82 + Math.floor(Math.random()*9));
  } else if(Math.random()<0.30){
    const i = Math.floor(Math.random()*foods.length);
    Math.random()<0.5 ? (foods[i].temp = +(9 + Math.random()*3).toFixed(1))
                      : (foods[i].hum  = 82 + Math.floor(Math.random()*9));
  }
}
const tbody=document.getElementById('rows');
function drawTable(){
  tbody.innerHTML='';
  foods.forEach(f=>{
    const st=classify(f.temp,f.hum);
    const tr=document.createElement('tr');
    tr.innerHTML=`<td>${f.name}</td>
                  <td>${f.temp.toFixed(1)}°C</td>
                  <td>${f.hum}%</td>
                  <td><span class="chip ${st.cls}">${st.label}</span></td>`;
    tbody.appendChild(tr);
  });
}
function step(){
  foods.forEach(f=>{
    f.temp = Math.max(0, Math.min(12, f.temp + (Math.random()*0.8-0.4)));
    f.hum  = Math.max(35, Math.min(90,  f.hum  + Math.floor(Math.random()*7-3)));
  });
  ensureUnsafe();
  drawTable();
}
drawTable();
setInterval(step, 5000);
</script>
</body>
</html>
""".replace("%FOOD_NAMES%", json.dumps(FOOD_NAMES))

# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template_string(home_html)

@app.route("/foods")
def foods_page():
    return render_template_string(foods_html)

@app.route("/simulate")
def simulate():
    return render_template_string(simulate_html)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
