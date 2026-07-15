import requests
from bs4 import BeautifulSoup
import json

workshops = []

# 1. Scrape the teacher training center
try:
    url = "https://www.iots.tc.edu.tw/"
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")

    for item in soup.select("li, div.news-item, tr"):
        title_tag = item.find("a")
        title = title_tag.get_text(strip=True) if title_tag else ""
        link = title_tag.get("href", "") if title_tag else ""
        date_tag = item.find("span", class_="date") or item.find("td", class_="date")
        date = date_tag.get_text(strip=True) if date_tag else ""

        if title:
            workshops.append({
                "title": title,
                "date": date,
                "unit": "臺中市 教師研習中心",
                "link": link
            })
except Exception as e:
    print(f"Failed to scrape iots.tc.edu.tw: {e}")

# 2. Scrape school announcement pages
school_ids = [
    "skgjh",   # 神岡國中
    "dyps",    # 大勇國小
    "dmjh",    # 大明國中
    "taes",    # 泰安國小
    # add more IDs here...
]

base_url = "https://school.tc.edu.tw/open-message/{}"

for sid in school_ids:
    url = base_url.format(sid)
    try:
        response = requests.get(url)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")

        for item in soup.select("li, div.news-item, tr"):
            title_tag = item.find("a")
            title = title_tag.get_text(strip=True) if title_tag else ""
            link = title_tag.get("href", "") if title_tag else ""
            date_tag = item.find("span", class_="date") or item.find("td", class_="date")
            date = date_tag.get_text(strip=True) if date_tag else ""

            if title:
                workshops.append({
                    "title": title,
                    "date": date,
                    "unit": sid,   # school ID (map to full name if you want)
                    "link": link
                })
    except Exception as e:
        print(f"Failed to scrape {sid}: {e}")

# Save results
with open("workshops.json", "w", encoding="utf-8") as f:
    json.dump(workshops, f, ensure_ascii=False, indent=2)

print("workshops.json updated from iots.tc.edu.tw and school.tc.edu.tw")
