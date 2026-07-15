import requests
from bs4 import BeautifulSoup
import json

workshops = []

# 1. Scrape the teacher training center (iots.tc.edu.tw)
try:
    # Target the actual index/news subpage directly where posts are listed
    url = "https://www.iots.tc.edu.tw/index/news"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=15)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "lxml")
    
    # Selecting the anchor tags that point to actual news items
    # Typically they are inside a list or a news table on this CMS
    links = soup.find_all("a", href=True)
    for link_tag in links:
        title = link_tag.get_text(strip=True)
        link = link_tag.get("href", "")
        
        # Avoid navigation bar items by excluding typical menu links
        if not title or len(title) < 5 or any(x in link for x in ["/device-admin", "/software", "/contact-us", "/kpi"]):
            continue
            
        # Format links
        if not link.startswith("http"):
            link = f"https://www.iots.tc.edu.tw{link}"
            
        workshops.append({
            "title": title,
            "date": "最新資訊",
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
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=15)
        response.encoding = "utf-8"
        soup = BeautifulSoup(response.text, "lxml")
        
        # School.tc.edu.tw uses tables with rows (tr) for announcements
        for row in soup.select("tr"):
            title_tag = row.find("a")
            if not title_tag:
                continue
                
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href", "")
            
            if not title or len(title) < 4:
                continue
                
            if not link.startswith("http"):
                link = f"https://school.tc.edu.tw{link}"
                
            # Date is usually in a sibling column (td)
            date_tag = row.find("span", class_="date") or row.find("td", class_="date")
            date = date_tag.get_text(strip=True) if date_tag else "未知日期"
            
            # Map school ID to a nicer title
            school_name = {
                "skgjh": "神岡國中",
                "dyps": "大勇國小",
                "dmjh": "大明國中",
                "taes": "泰安國小"
            }.get(sid, sid.upper())

            workshops.append({
                "title": title,
                "date": date,
                "unit": school_name,
                "link": link
            })
    except Exception as e:
        print(f"Failed to scrape school {sid}: {e}")

# Save results
with open("workshops.json", "w", encoding="utf-8") as f:
    json.dump(workshops, f, ensure_ascii=False, indent=2)

print(f"Scraped {len(workshops)} total items successfully.")
