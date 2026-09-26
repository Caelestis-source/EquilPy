import sqlite3
import pandas as pd

def get_databases(db_path='properties.db'):
    conn = sqlite3.connect(db_path)
    df_komp = pd.read_sql_query("SELECT * FROM antoine_constants", conn)
    df_int = pd.read_sql_query("SELECT * FROM van_laar_constants", conn)
    conn.close()
    return df_komp, df_int