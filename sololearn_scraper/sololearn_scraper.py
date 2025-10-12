import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

USERNAME = "26923151"
URL = f"https://www.sololearn.com/profile/{USERNAME}/?ref=app"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

# 이름과 XP 선택자 반영
name = soup.select_one("p.sl-p-details__name--text")
points = soup.select_one("span[sl-test-data='lblXPCount']")

# 랭크 부분은 아직 확인되지 않아 일시적으로 N/A 처리
rank = None

data = {
    "username": USERNAME,
    "name": name.text.strip() if name else "N/A",
    "points": points.text.strip() if points else "N/A",
    "rank": rank.text.strip() if rank else "N/A",
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

# 1️⃣ JSON 파일 저장 (기존 코드 그대로 유지)
with open("sololearn_scraper/sololearn_leaderboard.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Sololearn 리더보드 데이터 저장 완료:")
print(data)

# 2️⃣ README.md 업데이트 추가 (여기만 새로 추가)
readme_content = f"""
## 🧠 Sololearn Leaderboard (자동 업데이트)
> 이 데이터는 GitHub Actions로 매일 자동 갱신됩니다.

| Username | Name | XP | Rank | Last Updated |
|-----------|------|----|------|---------------|
| {data['username']} | {data['name']} | {data['points']} | {data['rank']} | {data['last_updated']} |
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)
