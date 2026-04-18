import os
import subprocess
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path
from app.core.config import settings

def backup_database():
    """
    Automates PostgreSQL database backup using pg_dump.
    """
    # Create backups directory
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)

    # Parse Database URL
    # Handle postgresql+asyncpg:// format
    url = settings.DATABASE_URL.replace("+asyncpg", "")
    parsed = urlparse(url)
    
    db_name = parsed.path.strip("/")
    db_user = parsed.username
    db_password = parsed.password
    db_host = parsed.hostname
    db_port = parsed.port or 5432

    # Filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = backup_dir / f"backup_{db_name}_{timestamp}.sql"
    compressed_file = f"{backup_file}.gz"

    print(f"Starting backup for database: {db_name}...")

    # Set password environment variable for pg_dump
    env = os.environ.copy()
    if db_password:
        env["PGPASSWORD"] = db_password

    try:
        # Run pg_dump
        # Shell=True is used to support compression via pipe if needed, 
        # but here we use subprocess.run for better control
        cmd = [
            "pg_dump",
            "-h", db_host,
            "-p", str(db_port),
            "-U", db_user,
            "-F", "c",  # Custom format (compressed)
            "-f", str(backup_file),
            db_name
        ]
        
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Backup successful: {backup_file}")
            # In a professional setup, we would upload to S3 here
            return str(backup_file)
        else:
            print(f"Backup failed: {result.stderr}")
            return None

    except Exception as e:
        print(f"An error occurred during backup: {str(e)}")
        return None

if __name__ == "__main__":
    backup_database()
