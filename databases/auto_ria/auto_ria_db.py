import subprocess

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy_utils import database_exists, create_database

from configs.auto_ria_config import DB_URL
from databases.auto_ria.auto_ria_tables import auto_ria


class AutoRiaDB:
    """ This is a class for working with a database """
    __instance = None

    def __new__(cls, *args, **kwargs):
        """ Create a new instance if it does not exist, otherwise, return the existing one """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, url):
        self.engine = create_engine(url)

    def create_db(self, meta):
        if not database_exists(self.engine.url):
            create_database(self.engine.url)
            print("Create DB")
        meta.create_all(self.engine)

    def add_auto_to_auto_ria_table(
            self,
            url: str,
            title: str,
            price_usd: int,
            odometer: int,
            username: str,
            phone_number: list,
            image_url: str,
            images_count: int,
            car_number: str,
            car_vin: str,
    ):
        with self.engine.connect() as db:
            db.execute(
                insert(auto_ria).
                    values(
                    url=url,
                    title=title,
                    price_usd=price_usd,
                    odometer=odometer,
                    username=username,
                    phone_number=phone_number,
                    image_url=image_url,
                    images_count=images_count,
                    car_number=car_number,
                    car_vin=car_vin,
                ).on_conflict_do_nothing()
            )
            db.commit()

    @staticmethod
    def dump_the_auto_ria_db():
        try:
            subprocess.run(f'pg_dump {DB_URL} > ./auto_ria_dump_db.sql', shell=True)
        except Exception as e:
            print(e)
