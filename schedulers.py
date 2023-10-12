import threading
import time

from config import START_PAGE, SCRAPING_START_TIME, DUMP_DB_START_TIME
from data_base.db import dump_db
from scraping import scraping_auto_ria


def start_scraping():
    while True:
        current_time = time.strftime("%H:%M")

        if current_time == SCRAPING_START_TIME:
            scraping_auto_ria(START_PAGE)

        if current_time == DUMP_DB_START_TIME:
            dump_db()
            time.sleep(1)


def run_schedules():
    thread_scraping = threading.Thread(target=start_scraping)
    thread_scraping.start()
