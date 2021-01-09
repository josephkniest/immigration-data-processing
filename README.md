# Immigration data insertion

Insert immigration data into a couple of useful postgres tables for better
immigration info aquisition

## Purpose

There is a dataset containing loose information about many visits through customs. It is
in the format of a csv file but the columns are quite nondecript and the data therein
is not intuitive to the reader. For example under "i94mode" which actually means the
mode by which the visitor entered the country there are just numbers, 1.0, 2.0, 3.0

To make this data much more useful we place it in a formal postgres database with the
etl. The schema for the tables are described below but the columns are designed to normalize
and make the raw data from the csv more holistic and much easier to understand, especially
someone who is looking at the data for the first time.

## Justification for the tools and techniques used

This is a fairly straightforward ETL. Python is probably the simplist platform to write
programs for, so it was used to compose said ETL with little overhead.

Since the data is not vast, a single local postgres instance is used to store the data.
Of course if the data were to become immense over time the storage medium would need
to be revisited. See the end section for more information on that.

#### Step 1: Scope the Project and Gather Data

The raw data came from the customs law enforcement agency. It is in the form of a csv file
with some but not too many missing values. To match the visit records up with airport information
the airpots csv file records are inserted into another table called "airports" so that customs
officials can cross reference the visit with an airport and have all the information on said
airport, potentially populating a web view.

#### Step 2: Explore and Assess the Data

This involved closely examining the csv files and looking up the column descriptions in the
column description file (which is not included here as the columns we care about are already
documented)

An opportunity to get additional information on the visitor's port of entry also made itself
available through the use of the "port" column

#### Step 3: Define the Data Model

From the analysis step the csv columns were sifted through to discover which columns contained
the most useful information for customs officials. As previously stated the raw data was not
as reader friendly as it could be so using the column description file this etl transforms
things like "reason for visit = 1.0" to "reason for visit = 'Business'"

#### Step 4: Run ETL to Model the Data

After the data model was defined, the etl composition process commenced. This was fairly quick
as the data model had already been defined and was simply a matter of using the varous
python3 functionality to convert and insert the desired data.

## Postgres

Both the default database name and postgres root user name are "postgres"

Connect locally thereto with ```psql postgresql://postgres:postgres@127.0.0.1/immigration```

#### Schema and data dictionary

visits: This table is the fact table that contains each i94 arrival through customs
  - visit_id: The serial ID of the visit instance (int)
  - port: Port of entry's international port code (varchar(4))
  - arrival_date: arrival timestamp (varchar(16)) - Source is number of days since 1/1/1960
  - depart_date: departure timestamp (varchar(16)) - Source is number of days since 1/1/1960
  - resident_state: The state code in which the traveler dwelled e.g. CA (varchar(2))
  - travel_mode: The visitor's travel mode, e.g. "Air", "Sea", "Land" (varchar(16))
  - age: Age of the visitor (int)
  - travel_purpose: Purpose of travel, "Business", "Pleasure", "Student" (varchar(16))
  - gender: Gender of the visitor (varchar(1))
  - airline: Code of the visitor' airline, if they travled by air (varchar(4))
  - visa: Visa code of the entry visa used by the visitor (varchar(4))

airports: This table contains a list of US airports
  - id: The unique international airport code e.g. LAX (varchar(4)) Need to strip off the "US-"
  - name: Name of the airport (varchar(192))
  - elevation_ft: Elevation in feet above sea level of the airport (int)
  - type: Type of airport, e.g. hellipad (varchar(64))
  - coordinates: Latitude and longitude of the airport (varchar(128))

#### Usage

This databse will be most helpful for customs officials to look through large swaths of visits.
They can use the arrival and departure dates to group visits together to get a larger perspective
on a particular visitor and understand whether any laws were violated.

The airpots table is useful for if immigration agents need to be dispatched to a location to
handle immigration law violations. For instance:

SELECT arrival_date, depart_date, visa, airline FROM visits

Might yield a record like this: ("4/1/2010", "4/1/2019", "WD", "LAX")

It may be that the "WD" visa only allows a visitor to remain in the country
for four years but this visitor clearly stayed in the LA area for 9 years and
violated immigration laws.

From there, using the "LAX" airport code immigration can run:

SELECT * from airport where id='LAX'

This will hand back the airport record for "LAX" including useful information like
the port's elevation and coordinates in case the official is unsure which airport
or which area the violator was in. 

## ETL

Create the postgres tables, then read the csv files and load the records from the csvs
into said tables. Columns will be processed as per the above column description

Execute with ```python3 ./etl.py```

## Data quality

To verify that the database does indeed contain data, run the following:

```python3 ./data-quality.py```

## Docker image

There's a docker image with the necessary instrumentation baked in (postgres, python 3)

1) Purge any images/containers with ```purge.sh```

2) Generate a new image with ```build.sh```

3) Fire up and get a bash session inside the container with ```run.sh```

## Performance

#### The data was increased by 100x

In this case we'll likely want to parallelize, or experiment with parallelizing the
insertions. Since the data records themselves are atomic, i.e. they do not rely on
one another this will only be bottlenecked by the database's write concurrency limits.

#### The pipelines would be run on a daily basis by 7 am every day.

This would require the upload of new data on a regular basis. The etl would also need
to move the responsibility of table creation to another program as we would be inserting
new visit records into postgres daily.

#### The database needed to be accessed by 100+ people.

A couple of options here. Vertical scaling, which is more expensive would just mean increasing
system resources on the postgres machine. Horizontal scaling would be putting several db instances
behind a load balancer. If the same database instance is desired we might look into a distributed
file system like HDFS instead of postgres for storage, that way we can scale up the cluster.


