"""
scraper.py - Fetches job listings from job boards using requests + BeautifulSoup.
"""

import requests
from bs4 import BeautifulSoup


def scrape_jobs(keywords: list[str]) -> list[dict]:
    """
    Scrapes remote job listings for each keyword.
    Returns a list of job dicts with title, company, url, and source.
    """
    all_jobs = []
    for keyword in keywords:
        jobs = _scrape_remoteok(keyword)
        all_jobs.extend(jobs)
    return all_jobs


def _scrape_remoteok(keyword: str) -> list[dict]:
    """
    Scrapes RemoteOK for jobs matching the keyword.
    RemoteOK is public and doesn't require login.
    """
    url = f"https://remoteok.com/remote-{keyword.replace(' ', '-')}-jobs"
    headers = {"User-Agent": "Mozilla/5.0"}  # required — sites block default Python requests

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # raises error if status code is 4xx/5xx
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    jobs = []

    # Each job listing is a <tr> tag with class "job"
    for row in soup.find_all("tr", class_="job"):
        title_tag = row.find("h2", itemprop="title")
        company_tag = row.find("h3", itemprop="name")
        link_tag = row.find("a", itemprop="url")

        # Only add the job if all fields are present
        if title_tag and company_tag and link_tag:
            jobs.append({
                "title": title_tag.text.strip(),
                "company": company_tag.text.strip(),
                "url": "https://remoteok.com" + link_tag["href"],
                "source": "RemoteOK"
            })

    return jobs
