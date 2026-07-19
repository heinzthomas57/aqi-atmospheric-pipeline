import os 
import sqlite3 
from pipeline import DB_NAME 
def test_database_infrastructure_exists():
    """Data Quality Gate: Verifies the relational database file exists on disk."""
    assert os.path.exists(DB_NAME) == True

def test_telemetry_payload_integrity():
    """Data Quality Gate: Verifies table rows exist and numbers are within realistic limits."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    #pull the latest entry loaded by your pipeline 
    cursor.execute("SELECT aqi, latitude, longitude from aqi_telemetry ORDER BY id DESC LIMIT 1")
    record = cursor.fetchone()
    conn.close()

    #Ensure we actually returneddata 
    assert record is not None 

    aqi, lat, lon = record 
    assert aqi >= 0
    assert 39.0 <= lat <= 41.0 
    assert -106.0 <= lon <= -104.0 