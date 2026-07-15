import requests
from bs4 import BeautifulSoup
import json

url = "https://www.iots.tc.edu.tw/"  # Taichung teacher training site

response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")

workshops = []

# Example: find spans with class names like "C9DxTc aw5Odc"
for item in soup.select("span.C9DxTc.aw5Odc"):
    title = item.get_text(strip=True)

    # Try to find a link near the span
    link_tag = item.find_parent().find("a") if item.find_parent() else None
    link = link_tag.get("href", "") if link_tag else ""

    # Try to find a date nearby
    date_tag = item.find_parent().find("span", class_="date") if item.find_parent() else None
    date = date_tag.get_text(strip=True) if date_tag else ""

    if title:
        workshops.append({
            "title": title,
            "date": date,
            "link": link
        })

# Save results
with open("workshops.json", "w", encoding="utf-8") as f:
    json.dump(workshops, f, ensure_ascii=False, indent=2)

print("workshops.json updated from iots.tc.edu.tw")
