from configs.auto_ria_config import DB_URL
from databases.auto_ria.auto_ria_db import AutoRiaDB
from databases.auto_ria.auto_ria_tables import meta
from schedulers.auto_ria_schedulers import run_schedules

if __name__ == '__main__':
    db = AutoRiaDB(url=DB_URL)
    db.create_db(meta=meta)
    run_schedules(db)
