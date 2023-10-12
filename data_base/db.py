import subprocess

import sqlalchemy
from sqlalchemy import create_engine, MetaData, Column, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.testing.schema import Table
from sqlalchemy_utils import database_exists, create_database

from data_base.db_engine import engine, DB_URL

meta = MetaData()

auto_ria = Table('auto_ria', meta,
                 Column('id', sqlalchemy.Integer, sqlalchemy.Sequence("id_seq"), unique=True),
                 Column('url', sqlalchemy.String(), unique=True),
                 Column('title', sqlalchemy.String()),
                 Column('price_usd', sqlalchemy.Integer()),
                 Column('odometer', sqlalchemy.Integer()),
                 Column('username', sqlalchemy.String(100)),
                 Column('phone_number', sqlalchemy.ARRAY(sqlalchemy.String(13))),
                 Column('image_url', sqlalchemy.String()),
                 Column('images_count', sqlalchemy.SmallInteger()),
                 Column('car_number', sqlalchemy.String(10)),
                 Column('car_vin', sqlalchemy.String(20)),
                 Column('datetime_found', sqlalchemy.DateTime(), server_default=func.now())
                 )


def create_db(engine: create_engine):
    if not database_exists(engine.url):
        create_database(engine.url)
        print("create")
    meta.create_all(engine)


def add_auto(
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
    with engine.connect() as db:
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


def dump_db():
    try:
        subprocess.run(f'pg_dump {DB_URL} > ./auto_ria_dump.sql', shell=True)
    except Exception as e:
        print(e)

