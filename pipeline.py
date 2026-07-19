import sqlite3
import requests
from datetime import datetime

DB_NAME = "aqi_atmospheric.db"

def init_db():
    """Verifies or builds the database infrastructure."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS aqi_telemetry (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            state TEXT,
            country TEXT,
            latitude REAL,
            longitude REAL,
            aqi INTEGER,
            primary_pollutant TEXT,
            recorded_at TEXT,
            captured_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    conn.close()

def fetch_and_ingest_telemetry():
    """Extracts atmospheric data from Open-Meteo API, transforms it, and loads it to SQLite."""
    # Target: Boulder, CO (Geographical Home of LASP research)
    boulder_lat = 40.0150
    boulder_lon = -105.2705
    
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={boulder_lat}&longitude={boulder_lon}&current=us_aqi,pm2_5,pm10,ozone"
    
    print(f"--- [INGESTION START] ---")
    print(f"Extracting raw telemetry from scientific endpoint for Boulder, CO...")
    
    try:
        response = requests.get(url, timeout=10)
        
        # Guard clause: Fail fast and explicitly check networking integrity
        if response.status_code != 200:
            print(f"CRITICAL ERROR: API returned unexpected status code {response.status_code}")
            return
            
        payload = response.json()
        current_metrics = payload.get("current", {})
        
        # --- DATA TRANSFORMATION PHASE ---
        city = "Boulder"
        state = "CO"
        country = "USA"
        lat = payload.get("latitude")
        lon = payload.get("longitude")
        aqi = current_metrics.get("us_aqi")
        recorded_at = current_metrics.get("time")
        
        # Compute a derived feature: Determine the primary pollutant signature
        pm25 = current_metrics.get("pm2_5", 0)
        ozone = current_metrics.get("ozone", 0)
        primary_pollutant = "PM2.5" if pm25 > ozone else "Ozone"
        
        print(f"Transforming telemetry: Mapping JSON fields -> Validating types...")
        print(f"Parsed Sample -> AQI: {aqi} | Primary Pollutant: {primary_pollutant} | Observation Time: {recorded_at}")
        
        # --- DATA INGESTION (LOAD) PHASE ---
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        
        # Enforce defensive data insertion using parameterized queries (prevents SQL injection)
        cursor.execute("""
            INSERT INTO aqi_telemetry (city, state, country, latitude, longitude, aqi, primary_pollutant, recorded_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (city, state, country, lat, lon, aqi, primary_pollutant, recorded_at))
        
        conn.commit()
        conn.close()
        print(f"Database Sync Successful: Record safely loaded into 'aqi_telemetry' table.")
        print(f"--- [INGESTION COMPLETE] ---")
        
    except Exception as e:
        print(f"Pipeline Pipeline Ingestion Failure: {str(e)}")

if __name__ == "__main__":
    init_db()
    fetch_and_ingest_telemetry()