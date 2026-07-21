import requests
from bs4 import BeautifulSoup
import json
import re

workshops = []

# Keywords to prioritize relevant posts
KEYWORDS = ["數位", "AI", "研習", "工作坊", "資訊", "學習", "精進"]

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# 1. Scrape the Teacher Training Center (iots.tc.edu.tw)
try:
    url = "https://www.iots.tc.edu.tw/index/news"
    response = requests.get(url, headers=headers, timeout=15)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    
    for item in soup.select("tr, li, .news-item"):
        title_tag = item.find("a")
        if not title_tag:
            continue
            
        title = title_tag.get_text(strip=True)
        link = title_tag.get("href", "")
        
        if not title or len(title) < 5 or any(nav in link for nav in ["/device-admin", "/software", "/contact-us", "/kpi", "index/news", "/workshop"]):
            continue
            
        if not link.startswith("http"):
            link = f"https://www.iots.tc.edu.tw{link}"
            
        date_tag = item.find("span", class_="date") or item.find("td", class_="date") or item.find("span")
        date = date_tag.get_text(strip=True) if date_tag else ""
        date_match = re.search(r"\d{4}-\d{2}-\d{2}|\d{3}-\d{2}-\d{2}", date)
        clean_date = date_match.group(0) if date_match else "最新資訊"

        workshops.append({
            "title": title,
            "date": clean_date,
            "unit": "臺中市教師研習中心",
            "link": link
        })
except Exception as e:
    print(f"Failed to scrape iots.tc.edu.tw: {e}")

# 2. Scrape Specific Schools (school.tc.edu.tw)
schools = {
    "064504": "臺中女中",
    "064748": "大元國小",
    "064741": "潭子國小",
    "064698": "長億高中",
    "064519": "大雅國中",
    "064712": "霧峰國小",
    "064502": "居仁國中",
    "064505": "光明國中",
    "064616": "太平國中",
    "064745": "大勇國小"
}

# --- MODIFICATION 1: Scan deeper pages (e.g., Pages 1 to 3) ---
MAX_PAGES = 3

for sid, sname in schools.items():
    for page in range(1, MAX_PAGES + 1):
        # Most school bulletin boards support ?page=N pagination
        url = f"https://school.tc.edu.tw/open-message/{sid}?page={page}"
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.encoding = "utf-8"
            soup = BeautifulSoup(response.text, "lxml")
            
            rows = soup.select("tr, .list-group-item")
            if not rows:
                break # Stop pagination if page is empty
                
            for row in rows:
                title_tag = row.find("a")
                if not title_tag:
                    continue
                    
                title = title_tag.get_text(strip=True)
                link = title_tag.get("href", "")
                
                if not title or len(title) < 4 or "open-message" not in link:
                    continue
                    
                if not link.startswith("http"):
                    link = f"https://school.tc.edu.tw{link}"
                    
                date_tag = row.find("span", class_="date") or row.find("td", class_="date") or row.find("span")
                date = date_tag.get_text(strip=True) if date_tag else ""
                date_match = re.search(r"\d{4}-\d{2}-\d{2}|\d{3}-\d{2}-\d{2}", date)
                clean_date = date_match.group(0) if date_match else "最新資訊"

                workshops.append({
                    "title": title,
                    "date": clean_date,
                    "unit": sname,
                    "link": link
                })
        except Exception as e:
            print(f"Failed to scrape school {sname} ({sid}) page {page}: {e}")

# --- MODIFICATION 2: Sort key posts to the top ---
# Sort posts that match target keywords to the top of the dataset
relevant_posts = [item for item in workshops if any(kw in item["title"] for kw in KEYWORDS)]
other_posts = [item for item in workshops if item not in relevant_posts]

# Prioritize relevant posts first, followed by recent general posts
final_workshops = relevant_posts + other_posts

# Save output
with open("workshops.json", "w", encoding="utf-8") as f:
    json.dump(final_workshops, f, ensure_ascii=False, indent=2)

print(f"Scraped total items: {len(final_workshops)} (Relevant items: {len(relevant_posts)})")
