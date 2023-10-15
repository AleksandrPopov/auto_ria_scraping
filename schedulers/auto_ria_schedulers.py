import threading
import time

from configs.auto_ria_config import START_PAGE, SCRAPING_START_TIME, DUMP_DB_START_TIME, STOP_PAGE
from scraping.auto_ria_scraping import AutoRiaScraping


def start_scraping(db):
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == SCRAPING_START_TIME:
            AutoRiaScraping.start_scraping_auto_ria(db=db, start_page=START_PAGE, stop_page=STOP_PAGE)


def start_dump(db):
    while True:
        current_time = time.strftime("%H:%M")
        if current_time == DUMP_DB_START_TIME:
            db.dump_the_auto_ria_db()
            time.sleep(60)


def run_schedules(db):
    thread_scraping = threading.Thread(target=start_scraping, args=(db,))
    thread_dump = threading.Thread(target=start_dump, args=(db,))

    thread_scraping.start()
    thread_dump.start()
