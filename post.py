import os
import requests
import random
from datetime import datetime, timezone, timedelta

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
event = os.environ.get("POST_EVENT", "AM")  # AM or PM

KST = timezone(timedelta(hours=9))
today = datetime.now(KST).strftime("%Y-%m-%d")

# 매일/슬롯(AM/PM)마다 결과가 바뀌되, 같은 날엔 재실행해도 같은 문구가 나오게 seed 고정
random.seed(f"{today}-{event}")

# --- 오전: 투자 멘탈케어(불안/조급함/흔들림 완화) ---
mood = ["불안", "조급함", "흔들림", "FOMO", "후회", "공포", "확신 과잉"]
frame = ["시장은 늘 변동한다", "변동성은 비용이 아니라 환경이다", "단기 등락은 소음이다", "내 계획이 내 안전벨트다"]
action = ["규칙부터 확인하자", "포지션을 줄이거나 늘리기 전에 근거를 적자", "손이 먼저 나가기 전에 호흡을 한 번 하자", "체크리스트 3개만 보고 결정하자"]
remind = ["‘잃지 않는 것’이 먼저다", "오늘의 목표는 ‘완벽’이 아니라 ‘일관성’이다", "한 번의 선택이 아니라 반복이 결과를 만든다", "시장은 내 감정을 시험하지만 내 원칙은 내가 지킨다"]

# --- 오후: 오늘 하루 수고 치하(자기효능/회복) ---
praise = ["오늘도 수고했어", "오늘도 잘 버텼다", "오늘 하루도 충분히 해냈다", "오늘의 너, 괜찮았다"]
detail = ["결과보다 과정이 쌓였다", "흔들릴 순간에도 중심을 잡으려 했다", "할 일만 하고 끝냈다", "감정에 끌려가지 않으려 했다"]
close = ["이제는 쉬어도 된다", "내일은 내일의 장이 열린다", "오늘은 여기까지면 충분하다", "루틴을 지킨 하루는 이미 이긴 하루다"]

if event == "AM":
    text = (
        f"🌅 {today} 아침 멘탈 체크\n"
        f"- 오늘의
