import requests
from bs4 import BeautifulSoup
import smtplib
import os
from email.message import EmailMessage

def get_ssc_updates():
    try:
        # Visiting the SSC official portal
        url = "https://ssc.gov.in/p/latest-news" 
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')
        # Finding the first 3 news items
        news_items = [item.text.strip() for item in soup.find_all('a', limit=3)]
        return "\n".join(news_items)
    except:
        return "Could not reach SSC site; check ssc.gov.in manually."

def send_report():
    EMAIL_ADDRESS = os.environ.get('EMAIL_USER')
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASS')
    
    # Scraped Live Update
    ssc_news = get_ssc_updates()

    body = f"FULLY AUTOMATED JOB TRACKER\n" + "="*30 + "\n\n"
    body += f"🔥 LIVE SSC UPDATES:\n{ssc_news}\n\n"
    body += "📍 OTHER TARGETED EXAMS (Static Check):\n"
    body += "- CDS/CAPF: Check upsc.gov.in\n- IBPS: Check ibps.in\n"
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = "Automated Job Alert - Sunday"
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = EMAIL_ADDRESS

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)

if __name__ == "__main__":
    send_report()
