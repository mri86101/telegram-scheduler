import os
import json
import random
import requests
from datetime import datetime, timezone, timedelta, date
import holidays

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
event = os.environ.get("POST_EVENT", "AM")  # AM or PM

# ---- 시간/오늘 날짜(KST) ----
KST = timezone(timedelta(hours=9))
now_kst = datetime.now(KST)
today = now_kst.date()

# ---- 실행 타입: 수동이면 무조건 발행 ----
is_manual = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"

# ---- 거래일 판단(자동 실행일 때만 적용) ----
kr_holidays = holidays.KR()  # 대체공휴일 포함
is_weekday = today.weekday() < 5
is_holiday = today in kr_holidays

# (선택) 거래소 특수 휴장일이 있으면 추가
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
            if not line:
                continue
            items.append(json.loads(line))
    if not items:
        raise ValueError(f"{path} is empty")
    return items

morning = load_jsonl("quotes_morning.jsonl")
afternoon = load_jsonl("quotes_afternoon.jsonl")

# ---- 같은 날/같은 슬롯은 같은 명언 ----
random.seed(f"{today.isoformat()}-{event}")

if event == "AM":
    q = random.choice(morning)
    text = (
        f"🌅 Morning Insight ({today})\n\n"
        f"“{q['en']}”\n"
        f"— {q['author']}\n\n"
        f"💬 {q['ko']}\n"
        f"🔪 {q['note']}"
    )
else:
    q = random.choice(afternoon)
    text = (
        f"🌇 Closing Reflection ({today})\n\n"
        f"“{q['en']}”\n"
        f"— {q['author']}\n\n"
        f"💬 {q['ko']}\n"
        f"🌿 {q['note']}"
    )

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
r = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
r.raise_for_status()
print("Sent!")
