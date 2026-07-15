import requests
from bs4 import BeautifulSoup
import json
import re

workshops = []

# 1. Scrape the teacher training center (iots.tc.edu.tw)
try:
    # Target the announcements page directly for more reliable listings
    url = "https://www.iots.tc.edu.tw/index/news" 
    response = requests.get(url, timeout=10)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    
    # Selecting the main table rows or list items in the content section
    # On most school sites, announcements are listed in a table <tbody> <tr> or .news-list
    for item in soup.select("tr, .news-list li, .card"):
        title_tag = item.find("a")
        if not title_tag:
            continue
            
        title = title_tag.get_text(strip=True)
        link = title_tag.get("href", "")
        
        # Only process if it relates to "數位學習"
        if "數位學習" in title:
            # Construct absolute URL
            if link and not link.startswith("http"):
                link = f"https://www.iots.tc.edu.tw{link}"
                
            date_tag = item.find("span", class_="date") or item.find("td", class_="date") or item.find("span")
            date = date_tag.get_text(strip=True) if date_tag else ""
            # Quick regex cleanup to extract dates like YYYY-MM-DD or 115-xx-xx if needed
            
            workshops.append({
                "title": title,
                "date": date,
                "unit": "臺中市教師研習中心",
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
]
base_url = "https://school.tc.edu.tw/open-message/{}"

for sid in school_ids:
    url = base_url.format(sid)
    try:
        response = requests.get(url, timeout=10)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")
        
        # school.tc.edu.tw typical structure: 
        # Usually list posts inside table rows <tr> or list items inside a .post-list / .announcement container
        for item in soup.select("tr, .list-group-item, .news-item"):
            title_tag = item.find("a")
            if not title_tag:
                continue
                
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href", "")
            
            if "數位學習" in title:
                if link and not link.startswith("http"):
                    link = f"https://school.tc.edu.tw{link}"
                    
                date_tag = item.find("span", class_="date") or item.find("td", class_="date")
                date = date_tag.get_text(strip=True) if date_tag else ""
                
                workshops.append({
                    "title": title,
                    "date": date,
                    "unit": sid.upper(),   
                    "link": link
                })
    except Exception as e:
        print(f"Failed to scrape {sid}: {e}")

# Save results
with open("workshops.json", "w", encoding="utf-8") as f:
    json.dump(workshops, f, ensure_ascii=False, indent=2)

print(f"workshops.json updated. Total found: {len(workshops)}")
