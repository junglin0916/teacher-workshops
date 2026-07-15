import requests
from bs4 import BeautifulSoup
import json

# Target site
url = "https://www.iots.tc.edu.tw/"

response = requests.get(url)
response.encoding = "utf-8"
soup = BeautifulSoup(response.text, "lxml")

workshops = []

# Example: find training announcements in the site structure
# Adjust selectors depending on the actual HTML layout
for item in soup.select("div.news-item, li"):  # try common containers
    title = item.get_text(strip=True)
    link_tag = item.find("a")
    link = link_tag["href"] if link_tag else ""
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
