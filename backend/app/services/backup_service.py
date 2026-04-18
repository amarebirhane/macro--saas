import os
import subprocess
from datetime import datetime
from urllib.parse import urlparse
from pathlib import Path
from app.core.config import settings
from app.core.logging_config import logger

async def run_database_backup():
    """
    Automates PostgreSQL database backup using pg_dump.
    This is an async wrapper intended for use by background workers.
    """
    # Create backups directory
    backup_dir = Path("backups")
    backup_dir.mkdir(exist_ok=True)

    # Parse Database URL
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

    logger.info(f"Starting background database backup for: {db_name}")

    # Set password environment variable
    env = os.environ.copy()
    if db_password:
        env["PGPASSWORD"] = db_password

    try:
        # Run pg_dump
        cmd = [
            "pg_dump",
            "-h", db_host,
            "-p", str(db_port),
            "-U", db_user,
            "-F", "c",
            "-f", str(backup_file),
            db_name
        ]
        
        # Use asyncio to run the subprocess safely if needed, but for simplicity:
        result = subprocess.run(cmd, env=env, capture_output=True, text=True)
        
        if result.returncode == 0:
            logger.info(f"Database backup successful: {backup_file}")
            return str(backup_file)
        else:
            logger.error(f"Database backup failed: {result.stderr}")
            return None

    except Exception as e:
        logger.error(f"An error occurred during background backup: {str(e)}")
        return None
