# AQI Atmospheric Telemetry Pipeline

An automated, test-backed data engineering pipeline designed to ingest, transform, and log scientific air quality indices (AQI) from external meteorological endpoints into a structured relational storage layout. 

This repository serves as a practical demonstration of Python ETL production patterns, relational schema design, automated data quality verification, and Linux command-line workflows.

## System Architecture

[ Open-Meteo Air Quality API ]  <-- (Scientific Telemetry Stream)
|
v  [ HTTP GET Request via Python 'requests' ]
+-------------------------------------------------------+
|                  pipeline.py Engine                   |
|  - Extract: Grabs raw JSON payload for Boulder, CO    |
|  - Transform: Validates types & computes features     |
|  - Load: Performs parameterized SQL database upserts  |
+-------------------------------------------------------+
|
+---> [ SQLite Database: aqi_atmospheric.db ]
|        (Structured Relational Data Storage)
|
v
+-------------------------------------------------------+
|                test_pipeline.py Suite                 |
|  - Programmatic Data Quality & Integrity Validation   |
|  - Assertions: Target bounding boxes & value limits   |
+-------------------------------------------------------+

## Production Engineering Design Patterns Implemented

* **Relational Storage Engine:** Avoided flat, unindexed text logging (CSV frameworks) by mapping out a clean relational schema inside an embedded `SQLite` backend.
* **Defensive Pipeline Coding:** Implemented proactive networking guard clauses to check response status codes and gracefully exit before system degradation occurs. 
* **Data Security & Injection Prevention:** Enforced parameterized query bindings (`?` tokens) rather than brittle, manual string formatting during database transactions.
* **Feature Derivation:** Implemented programmatic data transformation logic to dynamically evaluate and calculate the primary pollutant signature on incoming records.
* **Automated Data Quality Gates:** Utilized the industry-standard `pytest` framework to verify database file availability and perform rigorous boundary checks (such as geographical coordinate mapping limits) on captured rows.

## Local Workflow Deployment & Verification

### Ingest Live Telemetry
To execute the ETL script directly through the Linux command-line interface:
```bash
python3 pipeline.py

### Run Data Quality Assurances 
To trigger the automated testing framework and run validation assertions: 
``` Bash 
pytest test_pipeline.py 

4. Save your updated `README.md` file (`Ctrl + S` or `Cmd + S`).
5. Now, click back down into your **Terminal window** at the bottom to save this final piece of work to your GitHub profile[cite: 951]. Run these final 3 commands back-to-back:
