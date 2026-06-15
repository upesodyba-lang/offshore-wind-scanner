
import feedparser
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# -----------------------------
# CONFIG
# -----------------------------

EMAIL_FROM = "your_email@gmail.com"
EMAIL_TO = "your_email@gmail.com"
EMAIL_PASS = "your_app_password"   # important!

KEYWORDS_HIGH = [
    "offshore wind project", "wind farm", "GW",
    "Vestas", "Siemens Gamesa", "GE Vernova",
    "turbine failure", "blade failure", "gearbox failure",
    "floating wind"
]

KEYWORDS_MEDIUM = [
    "partnership", "supply chain", "manufacturing"
]

RSS_FEEDS = [
    "https://www.offshorewind.biz/feed/",
    "https://renews.biz/feed/"
]

# -----------------------------
# LOGIC
# -----------------------------

def classify(title):
    t = title.lower()
    for k in KEYWORDS_HIGH:
        if k.lower() in t:
            return "High"
    for k in KEYWORDS_MEDIUM:
        if k.lower() in t:
            return "Medium"
    return "Low"


def fetch():
    articles = []
    for url in RSS_FEEDS:
        feed = feedparser.parse(url)
        for e in feed.entries:
            articles.append({
                "title": e.title,
                "link": e.link,
                "date": getattr(e, "published", "Unknown")
            })
    return articles


def build_report(articles):
    now = datetime.now().strftime("%Y-%m-%d")

    high, med, low = [], [], []

    for a in articles:
        entry = f"{a['title']}\n{a['link']}\n"
        r = classify(a["title"])
        if r == "High":
            high.append(entry)
        elif r == "Medium":
            med.append(entry)
        else:
            low.append(entry)

    report = f"""
Offshore Wind Weekly Scanner
Date: {now}

High: {len(high)}
Medium: {len(med)}
Low: {len(low)}

=== HIGH ===
{''.join(high)}

=== MEDIUM ===
{''.join(med)}
"""

    return report


def send_email(text):
    msg = MIMEText(text)
    msg["Subject"] = "Offshore Wind Weekly Scanner"
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(EMAIL_FROM, EMAIL_PASS)
        server.send_message(msg)


# -----------------------------
# RUN
# -----------------------------

articles = fetch()
report = build_report(articles)
send_email(report)
