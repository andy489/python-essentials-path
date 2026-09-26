QUERIES = {
    "events": """
        CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        event_name TEXT NOT NULL,
        event_date TEXT NOT NULL,
        priority INTEGER NOT NULL,
        is_private BOOLEAN NOT NULL
    );
""",
}
