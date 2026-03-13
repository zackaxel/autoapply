"""
AutoApply - Job Board Scraper & Email Digest Tool
Run this file to start the daily job scraper.
"""

import schedule
import time
from modules.scraper import scrape_jobs
from modules.storage import init_db, save_jobs, get_new_jobs
from modules.email_sender import send_digest


def run_daily_job():
    print("Running job scrape...")
    raw_jobs = scrape_jobs(keywords=["remote python developer", "remote software engineer"])
    new_jobs = get_new_jobs(raw_jobs)  # filters out ones we've seen before
    if new_jobs:
        save_jobs(new_jobs)
        send_digest(new_jobs)
        print(f"Sent digest with {len(new_jobs)} new jobs.")
    else:
        print("No new jobs found today.")


if __name__ == "__main__":
    init_db()  # create the database table if it doesn't exist

    # Run once immediately, then every 24 hours
    run_daily_job()
    schedule.every(24).hours.do(run_daily_job)

    while True:
        schedule.run_pending()
        time.sleep(60)
