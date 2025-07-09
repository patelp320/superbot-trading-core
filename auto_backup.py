import shutil, datetime

def backup():
    shutil.copy("logs/trade_journal.csv", f"backups/trade_{datetime.date.today()}.csv")
