# ✈️ Flight Radar ETL Pipeline

![SQLite](https://img.shields.io/badge/database-sqlite-lightgrey)
![ETL](https://img.shields.io/badge/pipeline-ETL-green)

A configurable **ETL pipeline** that retrieves airport arrival data from the AeroDataBox API, validates and transforms the records, and stores them in a normalized SQLite database.

---

# 🚀 Project Overview

This project demonstrates the core components of a **data engineering pipeline**.

The pipeline performs the following steps:

- Extract flight data from an external API
- Transform raw JSON data into structured records
- Validate incomplete flight entries
- Normalize airline data
- Store results in a relational database

The pipeline is **configuration-driven**, meaning airports and API parameters can be modified without changing the code.

---

# ✨ Key Features

- Configurable ETL pipeline
- API integration
- Data validation layer
- Normalized database schema
- Logging and observability
- Modular architecture

---

# 🧠 Architecture

The project follows a modular ETL architecture:

```
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
```

Each module has a single responsibility, making the system easier to maintain and extend.

---

# 📁 Project Structure

```
ETL_Airports
│
├─ src
│   ├─ app.py
│   ├─ fetch_service.py
│   ├─ flight_row_transformer.py
│   ├─ db_storage.py
│   ├─ models.py
│   └─ logging_config.py
│
├─ logs
│   └─ pipeline.log
│
├─ flights.db
├─ config.json
└─ README.md
```

---

# 📦 File Responsibilities

| File                        | Responsibility                     |
| --------------------------- | ---------------------------------- |
| `app.py`                    | Orchestrates the ETL pipeline      |
| `fetch_service.py`          | Retrieves flight data from the API |
| `flight_row_transformer.py` | Cleans and validates flight data   |
| `db_storage.py`             | Handles SQLite persistence         |
| `models.py`                 | Defines the `FlightRecord` model   |
| `logging_config.py`         | Configures application logging     |
| `config.json`               | Defines API settings and airports  |

---

# 🔄 ETL Pipeline Flow

```
Run script
      ↓
Load configuration
      ↓
Fetch raw API data
      ↓
Validate and transform flight records
      ↓
Normalize airline data
      ↓
Insert records into SQLite database
      ↓
Log processing results
```

---

# 🗄 Database Schema

## flights

| Column              | Description                      |
| ------------------- | -------------------------------- |
| id                  | Primary key                      |
| destination_airport | Airport being monitored          |
| origin_country      | Country of departure             |
| origin_iata_airport | Departure airport                |
| flight_number       | Airline flight identifier        |
| airline_id          | Foreign key referencing airlines |
| year                | Arrival year                     |
| month               | Arrival month                    |
| day                 | Arrival day                      |
| hour                | Arrival hour                     |
| minute              | Arrival minute                   |
| second              | Arrival second                   |

---

## airlines

| Column | Description  |
| ------ | ------------ |
| id     | Primary key  |
| name   | Airline name |

Flights reference airlines through `airline_id`.

---

# 🔐 Duplicate Protection

To prevent duplicate records, the database uses a unique constraint:

UNIQUE(destination_airport, flight_number, year, month, day, hour, minute)

This allows the pipeline to run multiple times without inserting identical records.

---

# 🔎 Data Validation

During transformation the pipeline verifies that each flight record contains all required fields.

A record is skipped if any of the following are missing:

- origin country
- origin airport
- flight number
- airline name
- arrival timestamp

Skipped records are reported through the logging system.

---

# ⚙️ Configuration

All pipeline parameters are defined in `config.json`.

Example configuration:

```json
{
  "api": {
    "base_url": "https://aerodatabox.p.rapidapi.com/flights/airports",
    "timeout_seconds": 1200,
    "range_hours": 6,
    "airports": ["BER", "LEJ", "CPH"]
  }
}
```

This allows the pipeline to run against any airport list without changing the code.

---

# 📜 Logging

The pipeline uses Python's built-in logging module instead of print statements.

Example output:

```
2026-03-12 10:41:03 | INFO | flight_pipeline | Processing airport LEJ
2026-03-12 10:41:05 | INFO | flight_pipeline | Fetched: 120
2026-03-12 10:41:05 | INFO | flight_pipeline | Valid records: 115
2026-03-12 10:41:05 | INFO | flight_pipeline | Skipped records: 5
2026-03-12 10:41:05 | INFO | flight_pipeline | Inserted into DB: 115
```

Logging improves observability, debugging and monitoring.

---

# 🔑 Environment Variables

API credentials are stored in .env.

API_KEY_RAPID=your_api_key_here

This prevents credentials from being committed to version control.

---

# ▶ Running the Project

Install dependencies:
pip install requests python-dotenv

Run the pipeline:
python app.py

---

# 🧰 Technologies Used

Python
SQLite
Requests
python-dotenv

---

# 👤 Author

capsgit

