import json
from datetime import date

# Temporary sample data until real scraping is added
workshops = [
    {
        "title": "數位學習精進方案研習 - 測試資料",
        "date": str(date.today()),
        "link": "https://www.tc.edu.tw/workshop/sample"
    }
]

with open("workshops.json", "w", encoding="utf-8") as f:
    json.dump(workshops, f, ensure_ascii=False, indent=2)

print("workshops.json updated")
