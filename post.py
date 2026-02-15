import os, json, random, requests, subprocess
from datetime import datetime, timezone, timedelta, date
import holidays

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
event = os.environ.get("POST_EVENT", "AM")  # AM or PM

KST = timezone(timedelta(hours=9))
now_kst = datetime.now(KST)
today = now_kst.date()

is_manual = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"

# ---- 거래일 체크(자동일 때만) ----
kr_holidays = holidays.KR()
is_weekday = today.weekday() < 5
is_holiday = today in kr_holidays
extra_market_closures = set([
    # date(2026, 12, 31),
])

if not is_manual:
    if (not is_weekday) or is_holiday or (today in extra_market_closures):
        print(f"Skip (not a trading day): {today} / holiday={is_holiday}")
        raise SystemExit(0)

def load_jsonl(path: str):
    items = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    if not items:
        raise ValueError(f"{path} is empty")
    return items

def load_history(path="history.json"):
    if not os.path.exists(path):
        return {"AM": [], "PM": []}  # list of {"d": "YYYY-MM-DD", "id": "..."}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_history(hist, path="history.json"):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(hist, f, ensure_ascii=False, indent=2)

def pick_quote(quotes, hist_slot, seed_key, exclude_last_n=100):
    # 최근 N개(=최근 N 거래일 발행분)에서 사용한 id 제외
    recent_ids = {x["id"] for x in hist_slot[-exclude_last_n:]}
    candidates = [q for q in quotes if q.get("id") not in recent_ids]
    pool = candidates if candidates else quotes  # 다 막히면(드물게) 전체에서
    random.seed(seed_key)
    return random.choice(pool)

def commit_if_needed(message: str):
    # 변경사항이 있으면 커밋 + 푸시
    subprocess.run(["git", "status", "--porcelain"], check=True, capture_output=True, text=True)
    st = subprocess.run(["git", "status", "--porcelain"], check=True, capture_output=True, text=True).stdout.strip()
    if not st:
        print("No changes to commit.")
        return
    subprocess.run(["git", "add", "history.json"], check=True)
    subprocess.run(["git", "commit", "-m", message], check=True)
    subprocess.run(["git", "push"], check=True)

morning = load_jsonl("quotes_morning.jsonl")
afternoon = load_jsonl("quotes_afternoon.jsonl")
hist = load_history()

seed_key = f"{today.isoformat()}-{event}"
if event == "AM":
    q = pick_quote(morning, hist["AM"], seed_key, exclude_last_n=100)
    text = (
        f"🌅 Morning Insight ({today})\n\n"
        f"🧠 {q['en']}\n"
        f"— Inspired by {q['author']}\n\n"
        f"💬 {q['ko']}\n"
        f"🔪 {q['note']}"
    )
else:
    q = pick_quote(afternoon, hist["PM"], seed_key, exclude_last_n=100)
    text = (
        f"🌇 Closing Reflection ({today})\n\n"
        f"🧠 {q['en']}\n"
        f"— Inspired by {q['author']}\n\n"
        f"💬 {q['ko']}\n"
        f"🌿 {q['note']}"
    )

# ---- 발송 ----
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
r = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
r.raise_for_status()
print("Sent:", q.get("id"))

# ---- history 업데이트(같은 날짜에 같은 슬롯은 중복 기록 안 함) ----
slot = "AM" if event == "AM" else "PM"
dstr = today.isoformat()
hist_slot = hist.get(slot, [])
if not any(x["d"] == dstr for x in hist_slot):
    hist_slot.append({"d": dstr, "id": q["id"]})
    hist[slot] = hist_slot
    save_history(hist)

    # 깃 커밋/푸시(워크플로 권한 필요)
    commit_if_needed(f"Update history ({slot}) {dstr}")
else:
    print("History already recorded for today/slot; skipping commit.")
