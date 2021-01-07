import os
import glob
import psycopg2
import json
import datetime
import math
import csv
from datetime import date, timedelta
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
        create table if not exists visits (
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


def dateTimeFromDaysSince1960(daysSince1960):
    """dateTimeFromDaysSince1960
    Get a datetime object representing the current date where the
    input is the number of elpased days since the 1st of Jan, 1960
    """
    start = date(1960, 1, 1)
    delta = timedelta(int(daysSince1960[:-2]))
    return (start + delta).strftime('%m/%d/%Y')

def process_visitors(conn):
    """process_visitors
    Opens the immigration visits file and loads records into visits table
    Parameters:
     - conn: (connection object) - Postgres db connection
    """
    cur = conn.cursor()
    travel_modes = {"1.0": "Air", "2.0": "Sea", "3.0": "Land", "9.0": "Not reported"}
    travel_purposes = {"1.0": "Business", "2.0": "Pleasure", "3.0": "Student"}
    with open("./immigration_data_sample.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        next(reader)
        for row in reader:
            print(row)
            port = row[6]
            arrival_date = dateTimeFromDaysSince1960(row[7])
            depart_date = dateTimeFromDaysSince1960(row[10])
            resident_state = row[9]
            travel_mode = travel_modes[row[8]]
            age = row[11]
            travel_purpose = travel_purposes[row[12]]
            gender = row[23]
            airline = row[25]
            visa = row[28]
            sql = """
                insert into visits (port, arrival_date, depart_date, resident_state, travel_mode, age, travel_purpose, gender, airline, visa)
                values ('{}', '{}', '{}', '{}', '{}', {}, '{}', '{}', '{}', '{}')
            """.format(port, arrival_date, depart_date, resident_state, travel_mode, age, travel_purpose, gender, airline, visa)
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
    process_visitors(conn)

    conn.close()


if __name__ == "__main__":
    main()

