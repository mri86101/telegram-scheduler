import os
import requests
import random
from datetime import datetime, timezone, timedelta

import holidays  # 추가

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
event = os.environ.get("POST_EVENT", "AM")

KST = timezone(timedelta(hours=9))
now_kst = datetime.now(KST)
today = now_kst.date()

# --- 실행 유형 구분 ---
is_manual = os.environ.get("GITHUB_EVENT_NAME") == "workflow_dispatch"

# --- 거래일 체크 (자동 실행일 때만 적용) ---
if not is_manual:
    if (not is_weekday) or is_holiday:
        print(f"Skip (not a trading day): {today} / holiday={is_holiday}")
        raise SystemExit(0)

# (선택) 한국거래소가 추가로 쉬는 날이 있으면 여기에 수동 추가 가능
extra_market_closures = set([
    # 예: date(2026, 12, 31),
])

if (not is_weekday) or is_holiday or (today in extra_market_closures):
    print(f"Skip (not a trading day): {today} / holiday={is_holiday}")
    raise SystemExit(0)

# ✅ 같은 날/같은 슬롯은 같은 문구로 고정
random.seed(f"{today.isoformat()}-{event}")

# --- 오전/오후 자동 생성(조합형) ---
mood = ["불안", "조급함", "흔들림", "FOMO", "후회", "공포", "확신 과잉"]
frame = ["시장은 늘 변동한다", "변동성은 환경이다", "단기 등락은 소음이다", "계획은 안전벨트다"]
action = ["규칙부터 확인하자", "근거를 한 줄로 적고 결정하자", "호흡 한 번 하고 클릭하자", "체크리스트 3개만 보고 움직이자"]
remind = ["‘잃지 않는 것’이 먼저다", "오늘의 목표는 ‘일관성’이다", "반복이 결과를 만든다", "원칙은 내가 지킨다"]

praise = ["오늘도 수고했어", "오늘도 잘 버텼다", "오늘 하루도 충분히 해냈다", "오늘의 너, 괜찮았다"]
detail = ["결과보다 과정이 쌓였다", "중심을 잡으려 했다", "할 일만 하고 끝냈다", "감정에 끌려가지 않으려 했다"]
close = ["이제는 쉬어도 된다", "내일은 내일의 장이 열린다", "오늘은 여기까지면 충분하다", "루틴을 지킨 하루는 이미 이긴 하루다"]

if event == "AM":
    text = (
        f"🌅 {today} 아침 멘탈 케어\n"
        f"- 오늘의 변수: {random.choice(mood)}\n"
        f"- 리마인드: {random.choice(frame)}\n"
        f"- 오늘의 행동: {random.choice(action)}\n"
        f"- 한 줄: {random.choice(remind)}"
    )
else:
    text = (
        f"🌇 {today} 오늘 마무리\n"
        f"{random.choice(praise)}. {random.choice(detail)}.\n"
        f"👉 {random.choice(close)}"
    )

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
r = requests.post(url, data={"chat_id": CHAT_ID, "text": text})
r.raise_for_status()
print("Sent!")
