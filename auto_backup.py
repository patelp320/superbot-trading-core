import os
import shutil
import datetime

LOG_DIR = os.environ.get("LOG_DIR", "logs")
BACKUP_DIR = "backups"


def backup() -> None:
    """Copy the daily trade journal to the backups folder if it exists."""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    journal = os.path.join(LOG_DIR, "trade_journal.csv")
    if os.path.exists(journal):
        dest = os.path.join(BACKUP_DIR, f"trade_{datetime.date.today()}.csv")
        shutil.copy(journal, dest)
