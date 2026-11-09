"""FMM codes page: live codes in green, expired ones in red with their dates, FMM logo colours, social buttons."""
import html, json
from pathlib import Path

STATE = Path(__file__).resolve().parent / "codes.json"
REDEEM = "https://redeem.fcm.ea.com"
LINKS = {  # menu sections; an empty url hides that button
    "Instagram": [("My Instagram", "https://www.instagram.com/fc_fmm/"), ("Instagram Community Chat", "")],
    "Facebook": [("Facebook Page", "https://www.facebook.com/61577183936749"),
                 ("Facebook Group", "https://www.facebook.com/groups/5916184738491385/")],
}
YOUTUBE = "https://www.youtube.com/@FC_FMM"


def latest(n=5, active=None):
    """Live codes first (newest first), then the most recently expired ones; n in total."""
    seen = json.loads(STATE.read_text(encoding="utf-8")).get("seen", {}) if STATE.exists() else {}
    live = {c["code"] for c in (active or [])}
    rows = [{**c, "live": c["code"] in live} for c in seen.values()]
    rows.sort(key=lambda c: c.get("first_seen", ""), reverse=True)
    rows.sort(key=lambda c: c.get("expired_on") or "", reverse=True)
    rows.sort(key=lambda c: not c["live"])
    return rows[:n]


def nice(d):
    import datetime as dt
    try:
        return dt.date.fromisoformat(d).strftime("%d %b %Y")
    except Exception:
        return d or ""


def page(rows, updated):
    e = html.escape
    def card(r):
        if r["live"]:
            meta = f"Added {e(nice(r.get('first_seen')))}"
            return f"""
  <div class="code live"><div class="top"><span class="tag">● LIVE NOW</span><span class="date">{meta}</span></div>
    <div class="name">{e(r['code'])}</div><div class="reward">{e(r.get('reward', ''))}</div>
    <button onclick="cp(this,'{e(r['code'])}')">Copy code</button></div>"""
        meta = f"Expired {e(nice(r.get('expired_on')))}" if r.get("expired_on") else f"Added {e(nice(r.get('first_seen')))}"
        return f"""
  <div class="code dead"><div class="top"><span class="tag">✕ EXPIRED</span><span class="date">{meta}</span></div>
    <div class="name">{e(r['code'])}</div><div class="reward">{e(r.get('reward', ''))}</div></div>"""
    cards = "".join(card(r) for r in rows) or '<p class="none">No codes right now. Follow FMM, we post every new code first.</p>'
    links = lambda sec: "".join(f'<a class="btn" href="{u}" target="_blank" rel="noopener">{e(l)} ➜</a>'
                                for l, u in LINKS[sec] if u)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>FC Mobile Codes | FMM</title>
<meta name="description" content="Latest FC Mobile redeem codes and rewards, updated every hour by FC Mobile Mania (FMM).">
<meta property="og:title" content="FC Mobile Codes by FMM"><meta property="og:image" content="logo.jpg">
<link rel="icon" href="logo.jpg">
<style>
:root{{--bg:#050505;--red:#E1062C;--purple:#8A2BE2;--white:#fff;--mut:#b4b4c0;--green:#00C853;--card:#101014}}
*{{box-sizing:border-box}}
body{{margin:0;color:var(--white);font-family:system-ui,-apple-system,Segoe UI,Roboto,sans-serif;min-height:100vh;
 background:radial-gradient(ellipse at 50% -10%,#5a0b7a66 0,transparent 55%),radial-gradient(ellipse at 50% 110%,#e1062c40 0,transparent 55%),var(--bg)}}
.wrap{{max-width:520px;margin:0 auto;padding:22px 16px 40px}}
header{{text-align:center}}
.logo{{width:112px;height:112px;border-radius:50%;box-shadow:0 0 0 4px var(--red),0 0 0 8px #fff,0 0 34px 10px #8a2be2aa;margin:6px auto 14px;display:block}}
h1{{font-size:30px;margin:0;font-weight:900;letter-spacing:.5px}}h1 span{{color:var(--red);text-shadow:0 0 18px #e1062c99}}
.sub{{color:var(--mut);font-size:13px;margin:6px 0 18px}}
.redeem{{display:block;text-align:center;background:var(--red);color:#fff;text-decoration:none;font-weight:900;padding:15px;border-radius:14px;
 font-size:17px;margin-bottom:20px;box-shadow:0 0 22px #e1062c66;letter-spacing:.3px}}
.code{{background:var(--card);border-radius:16px;padding:14px 16px;margin-bottom:12px;border:2px solid}}
.live{{border-color:var(--green);box-shadow:0 0 20px #00c85340}}
.dead{{border-color:#e1062c88;background:#1a070b}}
.top{{display:flex;justify-content:space-between;align-items:center;font-size:12px;color:var(--mut)}}
.tag{{padding:3px 9px;border-radius:8px;font-weight:900;font-size:12px}}
.live .tag{{background:var(--green);color:#002b12}}.dead .tag{{background:var(--red);color:#fff}}
.dead .date{{color:#ff6b81}}
.name{{font-size:28px;font-weight:900;letter-spacing:1px;margin:9px 0 2px;word-break:break-all}}
.dead .name{{color:#ff8a9a;text-decoration:line-through;text-decoration-thickness:2px}}
.reward{{color:var(--mut);font-size:15px;margin-bottom:12px}}.dead .reward{{margin-bottom:2px}}
button{{width:100%;padding:12px;border:0;border-radius:12px;background:var(--green);color:#002b12;font-weight:900;font-size:16px;cursor:pointer}}
.sec{{display:block;border-radius:16px;margin-bottom:12px;background:#0c0c10;border:2px solid #2a2a36;overflow:hidden;text-decoration:none;color:#fff}}
.sec>summary,a.sec{{list-style:none;cursor:pointer;display:flex;align-items:center;gap:12px;padding:16px;font-weight:900;font-size:19px}}
.sec>summary::-webkit-details-marker{{display:none}}
.sec>summary::after{{content:"▾";margin-left:auto;transition:transform .2s;color:var(--mut)}}.sec[open]>summary::after{{transform:rotate(180deg)}}
.ic{{width:38px;height:38px;border-radius:12px;display:grid;place-items:center;font-size:19px;flex:none}}
.n{{margin-left:auto;font-size:13px;color:var(--mut);font-weight:700}}.sec>summary .n{{margin-left:auto;margin-right:-4px}}
.codes{{border-color:var(--red);box-shadow:0 0 22px #e1062c44}}.codes .ic{{background:var(--red)}}
.ig .ic{{background:linear-gradient(45deg,#F58529,#DD2A7B,#8134AF)}}.ig[open]{{border-color:#DD2A7B}}
.fb .ic{{background:#1877F2}}.fb[open]{{border-color:#1877F2}}
.yt .ic{{background:#FF0000}}.yt{{border-color:#ff000066}}
.in{{padding:0 14px 14px}}
.btn{{display:block;text-align:center;color:#fff;text-decoration:none;font-weight:800;padding:14px;border-radius:12px;margin-top:10px;font-size:16px;background:#1d1d27;border:1.5px solid #3a3a4a}}
.ig .btn{{border-color:#DD2A7B}}.fb .btn{{border-color:#1877F2}}
h2{{font-size:15px;color:var(--mut);text-align:center;margin:26px 0 12px;letter-spacing:1px}}
.socials{{display:grid;grid-template-columns:1fr 1fr;gap:10px}}
.soc{{display:block;text-align:center;color:#fff;text-decoration:none;font-weight:800;padding:13px 8px;border-radius:12px;font-size:15px}}
.how{{color:var(--mut);font-size:14px;line-height:1.55;margin-top:22px;border-left:3px solid var(--purple);padding-left:12px}}.how b{{color:#fff}}
.none{{color:var(--mut);text-align:center}}footer{{text-align:center;color:#77778a;font-size:12px;margin-top:24px}}
</style></head><body><div class="wrap">
<header><img class="logo" src="logo.jpg" alt="FMM logo"><h1>FC MOBILE <span>CODES</span></h1>
<div class="sub">by FC Mobile Mania (FMM) · updated {e(updated)} (Bangladesh time)</div></header>
<details class="sec codes" open><summary><span class="ic">🎁</span>Redeem Codes<span class="n">{sum(r["live"] for r in rows)} live</span></summary>
<div class="in"><a class="redeem" href="{REDEEM}" target="_blank" rel="noopener">REDEEM AT redeem.fcm.ea.com ➜</a>
{cards}
<div class="how"><b>How to redeem:</b> copy a green code, open redeem.fcm.ea.com, log in with your EA account,
paste the code, then collect the reward from your FC Mobile inbox.</div></div></details>
<details class="sec ig"><summary><span class="ic">📸</span>Instagram</summary><div class="in">{links("Instagram")}</div></details>
<details class="sec fb"><summary><span class="ic">👍</span>Facebook</summary><div class="in">{links("Facebook")}</div></details>
<a class="sec yt" href="{YOUTUBE}" target="_blank" rel="noopener"><span class="ic">▶</span>YouTube<span class="n">➜</span></a>
<footer>Not affiliated with EA. Codes are checked every hour.</footer>
</div>
<script>function cp(b,c){{navigator.clipboard&&navigator.clipboard.writeText(c);b.textContent='Copied ✓';setTimeout(()=>b.textContent='Copy code',1500)}}</script>
</body></html>"""
