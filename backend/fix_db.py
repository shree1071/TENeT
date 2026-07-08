import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'data', 'tenet.db')
print(f"Modifying {db_path}...")
conn = sqlite3.connect(db_path)
c = conn.cursor()

try:
    c.execute('ALTER TABLE cat_regions ADD COLUMN nearest_clinic_km FLOAT')
    c.execute('ALTER TABLE cat_regions ADD COLUMN nearest_hospital_km FLOAT')
    c.execute('ALTER TABLE cat_regions ADD COLUMN healthcare_density INTEGER')
    c.execute('ALTER TABLE cat_regions ADD COLUMN has_specialist BOOLEAN')
    conn.commit()
    print("Added missing columns.")
except Exception as e:
    print(f"Error adding columns: {e}")

from database.config import SessionLocal
from services.data_importer import CATDataHandler

db = SessionLocal()
count, msg = CATDataHandler.calculate_static_healthcare_metrics(db)
print(f"ETL recalculation: {msg}")

db.close()
conn.close()
