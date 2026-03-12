✈️ Flight Radar ETL Pipeline

A configurable ETL pipeline that extracts airport arrival data from an aviation API and stores cleaned records in a normalized SQLite database.

🚀 Project Overview

This project implements a configurable and reproducible ETL pipeline.

The pipeline:

Extracts flight data from an aviation API

Validates and transforms raw JSON data

Normalizes airline information

Stores cleaned records in a relational database

The pipeline is fully configurable via JSON and can run for multiple airports.

🧠 Architecture
API (AeroDataBox)
        │
        ▼
 Fetch Layer
(fetch_service.py)
        │
        ▼
Transformation Layer
(flight_row_transformer.py)
        │
        ▼
 Storage Layer
(db_storage.py)
        │
        ▼
 SQLite Database
(flights.db)
📁 Project Structure
src
│
├── app.py
├── config.json
├── fetch_service.py
├── flight_row_transformer.py
├── models.py
├── db_storage.py
├── logging_config.py
├── flights.db
└── .env
File	Responsibility
app.py	Orchestrates the ETL pipeline
fetch_service.py	Fetches data from the API
flight_row_transformer.py	Cleans and validates flight data
db_storage.py	Handles SQLite persistence
models.py	Defines the FlightRecord model
logging_config.py	Configures application logging
🔄 ETL Pipeline Flow
Run script
   ↓
Load configuration
   ↓
Fetch raw API data
   ↓
Transform & validate flights
   ↓
Normalize airline data
   ↓
Insert records into database
   ↓
Log processing results
🗄 Database Schema
flights
Column	Description
destination_airport	Airport monitored
origin_country	Country of departure
origin_iata_airport	Departure airport
flight_number	Flight identifier
airline_id	Foreign key to airlines table
year	Arrival year
month	Arrival month
day	Arrival day
hour	Arrival hour
minute	Arrival minute
second	Arrival second
airlines
Column	Description
id	Primary key
name	Airline name

Flights reference airlines via airline_id.

🔐 Duplicate Protection

The database prevents duplicate flights using:

UNIQUE(destination_airport, flight_number, year, month, day, hour, minute)

This allows the ETL pipeline to run multiple times without inserting duplicate data.

🔎 Data Validation

The transformation layer validates each flight record.

A flight is skipped if any required field is missing:

origin country

origin airport

flight number

airline name

arrival timestamp

Invalid flights are reported through logging.

📜 Logging

The project uses Python's built-in logging module instead of print statements.

Example log output:

2026-03-12 10:41:03 | INFO | flight_pipeline | Processing airport: LEJ
2026-03-12 10:41:05 | INFO | flight_pipeline | Valid records: 115
2026-03-12 10:41:05 | INFO | flight_pipeline | Inserted into DB: 115

Logging improves:

observability

debugging

production readiness

⚙️ Configuration

Airports and API settings are defined in config.json.

Example:

{
  "api": {
    "base_url": "https://aerodatabox.p.rapidapi.com/flights/airports",
    "timeout_seconds": 1200,
    "range_hours": 6,
    "airports": ["BOG","LEJ","CPH"]
  }
}
🔑 Environment Variables

API credentials are stored in .env.

API_KEY_RAPID=your_api_key_here
▶ Running the Project

Install dependencies

pip install requests python-dotenv

Run the pipeline

python app.py
🧰 Technologies Used

Python

SQLite

Requests

python-dotenv

👤 Author

Christian Piñeros

💡 Possible Improvements

asynchronous API requests

caching

automatic retry logic

dashboard visualization

historical flight tracking

⭐ Result

This project demonstrates:

✔ ETL pipeline design
✔ API integration
✔ data validation
✔ relational database normalization
✔ logging and observability