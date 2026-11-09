"""Rebuilds index.html from the public code list on fcmobileforum.com (hourly GitHub Action). Made by FC Mobile Mania."""
import datetime as dt, html, json, re, urllib.request
from pathlib import Path
import codespage

URL = "https://fcmobileforum.com/fcmobile-redeem-codes"
UA = "FMM-code-page/1.0 (+https://nabilaraf41.github.io/fmm-codes/)"
HERE = Path(__file__).resolve().parent
STATE = HERE / "codes.json"


def active():
    page = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": UA}), timeout=30).read().decode("utf-8", "ignore")
    start, end = page.find("Active Codes"), page.find("Expired Codes")
    if start < 0 or end < 0:
        raise RuntimeError("layout changed")
    out = []
    for box in re.split(r'class="[^"]*codeBox[^"]*"', page[start:end])[1:]:
        code = re.search(r"redeemCode=([A-Za-z0-9]+)", box)
        reward = re.search(r'codeReward[^"]*">([^<]+)<', box)
        date = re.search(r'codeDate[^"]*">([^<]+)<', box)
        if code:
            out.append({"code": code.group(1).upper(), "reward": html.unescape(reward.group(1)).strip() if reward else "Free reward",
                        "date": html.unescape(date.group(1)).strip() if date else ""})
    return out


if __name__ == "__main__":
    st = json.loads(STATE.read_text(encoding="utf-8"))
    now = dt.datetime.now(dt.timezone(dt.timedelta(hours=6)))
    act = active()
    live = {c["code"] for c in act}
    for c in act:
        st["seen"].setdefault(c["code"], {"first_seen": now.date().isoformat(), **c}).pop("expired_on", None)
    for code, c in st["seen"].items():  # first run it drops off the site's active list = its expiry date
        if code not in live:
            c.setdefault("expired_on", now.date().isoformat())
    STATE.write_text(json.dumps(st, indent=1, ensure_ascii=False), encoding="utf-8")
    codespage.STATE = STATE
    old = (HERE / "index.html").read_text(encoding="utf-8") if (HERE / "index.html").exists() else ""
    new = codespage.page(codespage.latest(5, act), now.strftime("%d %b %Y, %H:%M"))
    body = lambda t: t.split("updated ", 1)[-1].split("</div>", 1)[-1]
    if body(old) != body(new):  # only rewrite when the codes changed (no hourly empty commits)
        (HERE / "index.html").write_text(new, encoding="utf-8")
    print("active:", [c["code"] for c in act])
