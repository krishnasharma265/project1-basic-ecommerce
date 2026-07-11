from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import READ_DB_URL,WRITE_DB_URL

write_db_url=WRITE_DB_URL
read_db_url=READ_DB_URL
write_engine=create_engine(write_db_url)
read_engine=create_engine(read_db_url)

write_sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=write_engine)
read_sessionlocal=sessionmaker(autocommit=False,autoflush=False,bind=read_engine)


Base=declarative_base()