# Immigration data insertion

Insert immigration data into a couple of useful postgres tables for better
immigration info aquisition

## Postgres

Both the default database name and postgres root user name are "postgres"

Connect locally thereto with ```psql postgresql://postgres:postgres@127.0.0.1/immigration```

#### Schema

visits: This table is the fact table that contains each i94 arrival through customs
  - visit_id: The serial ID of the visit instance
  - port: Port of entry's international port code (i94port)
  - arrival_date: arrival timestamp (arrdate) - Source is number of days since 1/1/1960
  - depart_date: departure timestamp (depdate) - Source is number of days since 1/1/1960
  - resident_state: The state code in which the traveler dwelled e.g. CA (i94addr)
  - travel_mode: The visitor's travel mode, e.g. "Air", "Sea", "Land" (i94mode)
  - age: Age of the visitor (i94bir)
  - travel_purpose: Purpose of travel, "Business", "Pleasure", "Student" (i94visa)
  - gender: Gender of the visitor (gendor)
  - airline: Code of the visitor' airline, if they travled by air (airline)
  - visa: Visa code of the entry visa used by the visitor (visatype)

airports: This table contains a list of US airports
  - id: The unique international airport code e.g. LAX (iso_region) Need to strip off the "US-"
  - name: Name of the airport (name)
  - elevation_ft: Elevation in feet above sea level of the airport (elevation_ft)
  - type: Type of airport, e.g. hellipad (type)
  - coordinates: Latitude and longitude of the airport (lat, lon)

## ETL

Create the postgres tables, then read the csv files and load the records from the csvs
into said tables. Columns will be processed as per the above column description

Execute with ```python3 ./etl.py```

## Docker image

There's a docker image with the necessary instrumentation baked in (postgres, python 3)

1) Purge any images/containers with ```purge.sh```

2) Generate a new image with ```build.sh```

3) Fire up and get a bash session inside the container with ```run.sh```
