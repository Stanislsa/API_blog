# import psycopg2

# from app.config import get_settings

# settings = get_settings()

# conninfo = f"user={settings.db_user} password={settings.db_password} host={settings.db_host} port={settings.db_port} dbname={settings.db_name}"

# def get_conn():
#     return psycopg2.connect(conninfo=conninfo)

import psycopg2
from app.config import get_settings

settings = get_settings()

# Create a connection string
conninfo = (
    f"dbname='{settings.db_name}' "
    f"user='{settings.db_user}' "
    f"password='{settings.db_password}' "
    f"host='{settings.db_host}' "
    f"port='{settings.db_port}'"
)

def get_conn():
    return psycopg2.connect(conninfo)
