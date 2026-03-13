# AutoApply 🤖

A Python automation tool that scrapes remote job listings daily and emails you a digest of new postings — so you never miss an opportunity.

## Features
- Scrapes remote job boards for keywords you define
- Stores seen jobs in a local SQLite database to avoid duplicate alerts
- Sends a clean HTML email digest with new listings every 24 hours
- Modular codebase — easy to add new job board scrapers

## Project Structure
autoapply/
├── main.py              # Entry point — runs the scheduler
├── requirements.txt     # Dependencies
└── modules/
    ├── scraper.py       # Fetches job listings from job boards
    ├── storage.py       # SQLite database for deduplication
    └── email_sender.py  # Builds and sends the email digest

## Setup
1. Clone the repo and install dependencies:
pip install -r requirements.txt

2. Open modules/email_sender.py and fill in your Gmail address and App Password.

3. Run the tool:
python main.py

## How It Works
1. main.py calls the scraper with your keywords
2. scraper.py fetches listings from RemoteOK using requests and parses HTML with BeautifulSoup
3. storage.py checks the SQLite database and filters out jobs already seen
4. New jobs are saved to the database and emailed via email_sender.py
5. schedule library re-runs the whole process every 24 hours

## Tech Stack
- Python 3.11+
- requests, BeautifulSoup4 (scraping)
- SQLite via sqlite3 (storage)
- smtplib (email)
- schedule (task scheduling)
