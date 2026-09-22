import sqlite3
import shutil
import os
from datetime import datetime

DB_PATH = "transport.db"
BACKUP_PATH = "transport.db.backup"


def migrate():
    if not os.path.exists(DB_PATH):
        print(f"Database {DB_PATH} does not exist yet. It will be created on startup.")
        return

    print(f"Creating backup of database to {BACKUP_PATH}...")
    shutil.copyfile(DB_PATH, BACKUP_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    def get_columns(table):
        cursor.execute(f"PRAGMA table_info({table});")
        return [row[1] for row in cursor.fetchall()]

    # 1. Migrate Admin
    admin_cols = get_columns("admin")
    if "username" not in admin_cols:
        print("Adding username to admin table...")
        cursor.execute("ALTER TABLE admin ADD COLUMN username VARCHAR;")
        cursor.execute("UPDATE admin SET username = lower(name) WHERE username IS NULL OR username = '';")
    if "email" not in admin_cols:
        print("Adding email to admin table...")
        cursor.execute("ALTER TABLE admin ADD COLUMN email VARCHAR;")

    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS ix_admin_username ON admin (username);")

    # 2. Migrate Bus
    bus_cols = get_columns("bus")
    if "route" not in bus_cols:
        print("Adding route to bus table...")
        cursor.execute("ALTER TABLE bus ADD COLUMN route VARCHAR;")
    if "is_active" not in bus_cols:
        print("Adding is_active to bus table...")
        cursor.execute("ALTER TABLE bus ADD COLUMN is_active BOOLEAN DEFAULT 1;")
        cursor.execute("UPDATE bus SET is_active = 1 WHERE is_active IS NULL;")

    # 3. Migrate Teacher
    teacher_cols = get_columns("teacher")
    if "department" not in teacher_cols:
        print("Adding department to teacher table...")
        cursor.execute("ALTER TABLE teacher ADD COLUMN department VARCHAR;")
    if "email" not in teacher_cols:
        print("Adding email to teacher table...")
        cursor.execute("ALTER TABLE teacher ADD COLUMN email VARCHAR;")
    if "phone" not in teacher_cols:
        print("Adding phone to teacher table...")
        cursor.execute("ALTER TABLE teacher ADD COLUMN phone VARCHAR;")
    if "is_active" not in teacher_cols:
        print("Adding is_active to teacher table...")
        cursor.execute("ALTER TABLE teacher ADD COLUMN is_active BOOLEAN DEFAULT 1;")
        cursor.execute("UPDATE teacher SET is_active = 1 WHERE is_active IS NULL;")

    # 4. Migrate Logs
    logs_cols = get_columns("logs")
    if "bus_id" not in logs_cols:
        print("Adding bus_id to logs table...")
        cursor.execute("ALTER TABLE logs ADD COLUMN bus_id INTEGER REFERENCES bus(id);")
        cursor.execute("""
            UPDATE logs 
            SET bus_id = (SELECT id FROM bus WHERE bus.name = logs.bus_name)
            WHERE bus_id IS NULL;
        """)
    cursor.execute("CREATE INDEX IF NOT EXISTS ix_logs_bus_id ON logs (bus_id);")

    # 5. Migrate Bills
    bills_cols = get_columns("bills")
    if "total_trips" not in bills_cols:
        print("Adding total_trips to bills table...")
        cursor.execute("ALTER TABLE bills ADD COLUMN total_trips INTEGER DEFAULT 0;")
    if "fare_per_trip" not in bills_cols:
        print("Adding fare_per_trip to bills table...")
        cursor.execute("ALTER TABLE bills ADD COLUMN fare_per_trip INTEGER DEFAULT 15;")
    if "status" not in bills_cols:
        print("Adding status to bills table...")
        cursor.execute("ALTER TABLE bills ADD COLUMN status VARCHAR DEFAULT 'unpaid';")
    if "created_at" not in bills_cols:
        print("Adding created_at to bills table...")
        cursor.execute("ALTER TABLE bills ADD COLUMN created_at DATETIME;")
        cursor.execute("UPDATE bills SET created_at = CURRENT_TIMESTAMP WHERE created_at IS NULL;")

    cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS uq_teacher_billing_month ON bills (teacher_id, billing_month);")

    conn.commit()
    conn.close()
    print("Database migration completed successfully!")


if __name__ == "__main__":
    migrate()
