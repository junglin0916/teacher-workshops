import requests
from bs4 import BeautifulSoup
import json

url = "https://www.iots.tc.edu.tw/"  # Taichung teacher training site

response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")

workshops = []

# Example selectors — adjust once we inspect the site structure
for item in soup.select("li, div.news-item"):
    title = item.get_text(strip=True)
    link_tag = item.find("a")
    link = link_tag.get("href", "") if link_tag else ""
    date_tag = item.find("span", class_="date")
    date = date_tag.get_text(strip=True) if date_tag else ""

    if title and link:
        workshops.append({
            "title": title,
            "date": date,
            "link": link
        })

# Save results
with open("workshops.json", "w", encoding="utf-8") as f:
    json.dump(workshops, f, ensure_ascii=False, indent=2)

print("workshops.json updated from iots.tc.edu.tw")
