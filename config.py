import os

URL = os.getenv('URL')

START_PAGE = int(os.getenv('START_PAGE'))

SCRAPING_START_TIME = os.getenv("SCRAPING_START_TIME")
DUMP_DB_START_TIME = os.getenv("DUMP_DB_START_TIME")

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
