import time
import random 
from bs4 import BeautifulSoup

import requests

import time
import requests


apikey = "441b3bd1605842819503790bdd91053ac050c3ca"
zenrows_api_base = "https://api.zenrows.com/v1/"

def scrape_search_results(name, location):
    # Format the search URL
    search_url = f"https://www.truepeoplesearch.com/results?name={name.replace(' ', '+')}&citystatezip={location.replace(' ', '+')}"
    
    response = requests.get(zenrows_api_base, params={
        "apikey": apikey,
        "url": search_url,
        "js_render": "true",
        "premium_proxy": "true"
    })
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract detail page URLs
    detail_links = soup.find_all("a", class_="detail-link")
    detail_urls = [f"https://www.truepeoplesearch.com{link.get('href')}" for link in detail_links]
    
    return detail_urls

def scrape_contact_info(detail_url):
    print("sleep before request")
    time.sleep(10)
    response = requests.get(zenrows_api_base, params={
        "apikey": apikey,
        "url": detail_url,
        "js_render": "true",
        "premium_proxy": "true"
    })
    print("request completed")
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract emails and phones from the detail page
    emails = []
    phones = []
    
    # Look for email links
    email_links = soup.find_all("a", href=lambda x: x and "@" in x and "mailto:" in x)
    emails = [link.get_text().strip() for link in email_links]
    
    # Look for phone links
    phone_links = soup.find_all("a", href=lambda x: x and "tel:" in x)
    phones = [link.get_text().strip() for link in phone_links]
    
    # Also search for emails in text content
    import re
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    page_text = soup.get_text()
    text_emails = re.findall(email_pattern, page_text)
    emails.extend(text_emails)
    
    return {
        "url": detail_url,
        "emails": list(set(emails)),  # Remove duplicates
        "phones": phones
    }

# Main execution
name = "Shelmadine Jones"
location = "Vallejo, CA"

print(f"Searching for {name} in {location}...")

# Get detail page URLs
detail_urls = scrape_search_results(name, location)
# print(detail_urls)

detail_urls = list(set(detail_urls))
print(detail_urls)  # Output may be unordered like ['b', 'a', 'c']


# Scrape each detail page
all_contacts = []
for url in detail_urls:
    print(f"Scraping: {url}")
    contact_info = scrape_contact_info(url)
    all_contacts.append(contact_info)
      # Be respectful with requests

# Print results
for contact in all_contacts:
    print(f"\nURL: {contact['url']}")
    print(f"Emails: {contact['emails']}")
    print(f"Phones: {contact['phones']}")
