
import httpx
import time
import sqlite3
from datetime import datetime, timezone

WEBSITES = [
    "https://google.com",
    "https://github.com",
    "https://microsoft.com"
]

DATABASE = "monitor.db"


def create_database():
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        CREATE TABLE IF NOT EXISTS monitoring_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            status TEXT NOT NULL,
            status_code INTEGER,
            response_time REAL,
            checked_at TEXT NOT NULL,
            error TEXT
        )
    """)

    connection.commit()
    connection.close()


def save_result(url, status, status_code, response_time, error=None):
    connection = sqlite3.connect(DATABASE)

    connection.execute("""
        INSERT INTO monitoring_history
        (url, status, status_code, response_time, checked_at, error)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        url,
        status,
        status_code,
        response_time,
        datetime.now(timezone.utc).isoformat(),
        error
    ))

    connection.commit()
    connection.close()


def check_website(url):
    print(f"\nChecking: {url}")

    start = time.perf_counter()

    try:
        response = httpx.get(
            url,
            timeout=10,
            follow_redirects=True
        )

        response_time = (time.perf_counter() - start) * 1000

        status = "UP" if 200 <= response.status_code < 400 else "DOWN"

        print(f"Status: {status}")
        print(f"HTTP Code: {response.status_code}")
        print(f"Response Time: {response_time:.2f} ms")

        save_result(
            url,
            status,
            response.status_code,
            response_time
        )

    except httpx.RequestError as error:
        response_time = (time.perf_counter() - start) * 1000

        print("Status: DOWN")
        print(f"Error: {error}")

        save_result(
            url,
            "DOWN",
            None,
            response_time,
            str(error)
        )


if __name__ == "__main__":

    create_database()

    print("WEBSITE HEALTH & UPTIME MONITOR")
    print("Database connected successfully!")

    while True:

        print("\nStarting monitoring cycle...")

        for website in WEBSITES:
            check_website(website)

        print("\nAll results saved to database.")
        print("Next check in 60 seconds...")

        time.sleep(60)
