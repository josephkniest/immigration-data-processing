import psycopg2
def main():
    # connect to sparkify database
    conn = psycopg2.connect("host=127.0.0.1 dbname=immigration user=postgres password=password")

    cur = conn.cursor()

    cur.execute("""
        select * from airports limit 1
    """)

    airport = None
    for rec in cur:
        airport = rec

    if airport is None:
        print("Airports database is empty")
    else:
        print("Airpots data inserted")

    cur.execute("""
        select * from visits limit 1
    """)

    visit = None
    for rec in cur:
        visit = rec

    if visit is None:
        print("Visits database is empty")
    else:
        print("Visits data inserted")

    conn.close()


if __name__ == "__main__":
    main()

