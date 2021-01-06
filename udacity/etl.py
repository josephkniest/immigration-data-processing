import os
import glob
import psycopg2
import json
import datetime
import math
from sql_queries import *

def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=postgres password=postgres")

    create_tables(conn)
    process_airports(conn)
    process_visitors(conn)    

    conn.close()


if __name__ == "__main__":
    main()

