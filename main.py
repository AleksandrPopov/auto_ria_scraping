import schedulers
from data_base.db import create_db
from data_base.db_engine import engine

create_db(engine=engine)
schedulers.run_schedules()
