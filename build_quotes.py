import json, random, hashlib

MORNING_AUTHORS = [
  "Warren Buffett","Charlie Munger","Peter Lynch","Ray Dalio","Howard Marks",
  "Benjamin Graham","Seth Klarman","Morgan Housel","George Soros","Paul Tudor Jones",
  "Jesse Livermore","John Bogle","Ed Seykota","Stan Druckenmiller","Aswath Damodaran"
]

AFTERNOON_AUTHORS = [
  "Warren Buffett","Charlie Munger","Howard Marks","Morgan Housel","John Bogle",
  "Ray Dalio","Peter Lynch","Seth Klarman","Benjamin Graham","Ed Seykota"
]

# 오전: 날카롭게(리스크/확률/규율/손실회피/포지션)
MORNING_TEMPLATES_EN = [
  "Your edge is not prediction; it's discipline under uncertainty.",
  "If you can't explain the downside, you don't own the position—you rent it.",
  "Volatility is the entry fee. Pay it calmly or don't enter.",
  "FOMO is a tax. Refuse to pay it.",
  "A good trade starts with an exit plan.",
  "Survival is compounding's first requirement.",
  "When you feel certain, cut position size—not corners.",
  "The market punishes haste more than ignorance.",
  "Risk is what remains after you think you're right.",
  "If your process breaks in stress, it wasn't a process."
]

MORNING_TEMPLATES_KO = [
  "우위는 예측이 아니라 불확실성 속 규율이다.",
  "하방을 설명 못하면 그 포지션은 ‘보유’가 아니라 ‘임대’다.",
  "변동성은 입장료다. 차분히 낼 수 없으면 들어가지 마라.",
  "FOMO는 세금이다. 내지 마라.",
  "좋은 매수는 좋은 출구 계획에서 시작한다.",
  "복리의 첫 조건은 생존이다.",
  "확신이 들수록 비중을 줄여라. 기준을 줄이지 말고.",
  "시장은 무지보다 조급함을 더 크게 벌준다.",
  "내가 맞다고 믿어도 남는 리스크가 진짜 리스크다.",
  "스트레스에서 무너지는 건 ‘프로세스’가 아니다."
]

MORNING_NOTES = [
  "오늘 매수/추매 전에: 손절·감내 범위·비중을 한 줄로 써라.",
  "결정 전 체크: 근거 1줄 + 반대근거 1줄. 둘 다 없으면 보류.",
  "오늘의 미션은 수익이 아니라 ‘실수 방지’다.",
  "포지션은 확신이 아니라 리스크로 조절한다.",
  "한 번 더: ‘틀렸을 때’ 계획이 있으면 들어가도 된다."
]

# 오후: 차분하게(회고/루틴/일관성/수고)
AFTERNOON_TEMPLATES_EN = [
  "A calm close is a win, regardless of the tape.",
  "You don't need perfect days; you need consistent ones.",
  "Today you protected your process. That's progress.",
  "Results fluctuate. Systems stay.",
  "Patience is an asset you can measure in actions.",
  "If you followed your rules, you earned the day.",
  "Compounding is built from ordinary, repeated restraint.",
  "You can rest when your decisions are explainable.",
  "You endured uncertainty. That's what investors do.",
  "A good night starts with a clean log."
]

AFTERNOON_TEMPLATES_KO = [
  "차분한 마감은 그 자체로 승리다.",
  "완벽한 하루보다 일관된 하루가 필요하다.",
  "오늘 프로세스를 지킨 건 분명한 전진이다.",
  "결과는 흔들려도 시스템은 남는다.",
  "인내는 행동으로 측정되는 자산이다.",
  "규칙을 지켰다면 오늘은 합격이다.",
  "복리는 평범한 절제의 반복에서 만들어진다.",
  "결정을 설명할 수 있다면 편히 쉬어도 된다.",
  "불확실성을 견뎠다. 그게 투자자의 일이다.",
  "좋은 밤은 기록이 깔끔할 때 시작한다."
]

AFTERNOON_NOTES = [
  "오늘의 성과: ‘무리한 한 번’이 아니라 ‘기준을 지킨 하루’다.",
  "내일을 위해: 오늘의 판단 1줄 요약만 남기고 종료.",
  "시장이 어땠든, 루틴을 지킨 당신은 잘했다.",
  "오늘의 교훈 하나만 챙기면 충분하다.",
  "자기비난 금지. 데이터만 남기자."
]

def make_id(prefix, author, en):
  h = hashlib.sha1(f"{prefix}|{author}|{en}".encode("utf-8")).hexdigest()[:10]
  return f"{prefix}-{h}"

def gen_block(prefix, authors, templ_en, templ_ko, notes, n):
  out = []
  for i in range(n):
    author = random.choice(authors)
    en = random.choice(templ_en)
    ko = random.choice(templ_ko)
    note = random.choice(notes)
    out.append({
      "id": make_id(prefix, author, en),
      "author": author,
      "en": en,
      "ko": ko,
      "note": note
    })
  # id 중복 제거(부족하면 더 뽑기)
  seen = set()
  uniq = []
  for q in out:
    if q["id"] not in seen:
      seen.add(q["id"])
      uniq.append(q)
  while len(uniq) < n:
    author = random.choice(authors)
    en = random.choice(templ_en)
    ko = random.choice(templ_ko)
    note = random.choice(notes)
    q = {"id": make_id(prefix, author, en), "author": author, "en": en, "ko": ko, "note": note}
    if q["id"] not in seen:
      seen.add(q["id"])
      uniq.append(q)
  return uniq[:n]

def dump_jsonl(path, items):
  with open(path, "w", encoding="utf-8") as f:
    for it in items:
      f.write(json.dumps(it, ensure_ascii=False) + "\n")

if __name__ == "__main__":
  random.seed(20260215)  # 고정 시드(원하면 바꿔도 됨)
  morning = gen_block("AM", MORNING_AUTHORS, MORNING_TEMPLATES_EN, MORNING_TEMPLATES_KO, MORNING_NOTES, 200)
  afternoon = gen_block("PM", AFTERNOON_AUTHORS, AFTERNOON_TEMPLATES_EN, AFTERNOON_TEMPLATES_KO, AFTERNOON_NOTES, 200)
  dump_jsonl("quotes_morning.jsonl", morning)
  dump_jsonl("quotes_afternoon.jsonl", afternoon)
  print("Generated 200/200 quotes.")
