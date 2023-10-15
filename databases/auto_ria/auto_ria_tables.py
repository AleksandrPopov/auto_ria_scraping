import sqlalchemy
from sqlalchemy import Table, Column, func, MetaData

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
