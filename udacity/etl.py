import os
import glob
import psycopg2
import json
import datetime
import math
import csv
def create_tables(conn):
    """create_tables
    Creates the airports and visitors tables
    Parameters:
     - conn: (connection object) - Postgres db connection
    """
    cur = conn.cursor()

    cur.execute("drop table if exists airports")
    cur.execute("""
        create table if not exists airports (
            id varchar(4) primary key not null,
            name varchar(192) not null,
            elevation_ft int not null,
            type varchar(64) not null,
            coordinates varchar(128) not null
        )
    """)

    cur.execute("drop table if exists visitors")
    cur.execute("""
        create table if not exists visitors (
            visit_id SERIAL primary key,
            port varchar(8) not null,
            arrival_date varchar(16) not null,
            depart_date varchar(16) not null,
            resident_state varchar(2) not null,
            travel_mode varchar(4) not null,
            age int not null,
            travel_purpose varchar(16) not null,
            gender varchar(1) not null,
            airline varchar(4),
            visa varchar(4) not null,
            foreign key(airline) references airports(id)
        )
    """)

def process_airports(conn):
    """create_tables
    Opens the airports file and loads records into airport table
    Parameters:
     - conn: (connection object) - Postgres db connection
    """
    cur = conn.cursor()

    with open("./airport-codes_csv.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            print(row)
            sql = """
                insert into airports (id, name, elevation_ft, type, coordinates)
                values ('{}', '{}', {}, '{}', '{}')
                on conflict (id) do nothing
            """.format(
                row[6][3:],
                row[2].replace("'", "''"),
                0 if row[3] == "" else row[3],
                row[1],
                row[10]
            )
            print(sql)
            cur.execute(sql)



def main():

    # connect to default database
    conn = psycopg2.connect("host=127.0.0.1 dbname=postgres user=postgres password=password")
    conn.set_session(autocommit=True)
    cur = conn.cursor()

    # create immigration database with UTF8 encoding
    cur.execute("DROP DATABASE IF EXISTS immigration")
    cur.execute("CREATE DATABASE immigration WITH ENCODING 'utf8' TEMPLATE template0")

    # close connection to default database
    conn.close()

    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=immigration user=postgres password=password")

    print(conn)

    create_tables(conn)
    process_airports(conn)
    #process_visitors(conn)    

    conn.close()


if __name__ == "__main__":
    main()

