import os
import requests
from bs4 import BeautifulSoup
import json
from datetime import datetime

# ✅ GitHub Secrets 에서 값 불러오기
USERNAME = os.getenv("SOLOLEARN_USER", "hidden")
URL = f"https://www.sololearn.com/profile/{USERNAME}/?ref=app"

headers = {"User-Agent": "Mozilla/5.0"}
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

name = soup.select_one("p.sl-p-details__name--text")
points = soup.select_one("span[sl-test-data='lblXPCount']")
rank = None

data = {
    # username은 JSON에 포함하지만 공개는 안 함
    "username": "hidden",  # ✅ 실제 값은 숨김
    "name": name.text.strip() if name else "N/A",
    "points": points.text.strip() if points else "N/A",
    "rank": rank.text.strip() if rank else "N/A",
    "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}

with open("sololearn_scraper/sololearn_leaderboard.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print("✅ Sololearn 리더보드 데이터 저장 완료:")
print(data)

readme_content = f"""
## 🧠 Sololearn Leaderboard (자동 업데이트)
> 이 데이터는 GitHub Actions로 매일 자동 갱신됩니다.

| Name | XP | Rank | Last Updated |
|------|----|------|---------------|
| {data['name']} | {data['points']} | {data['rank']} | {data['last_updated']} |
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme_content)
