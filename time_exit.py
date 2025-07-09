def should_exit(entry_time, now, limit=300):
    return (now - entry_time).seconds > limit
