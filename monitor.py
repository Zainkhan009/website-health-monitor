
import httpx
import time
import sqlite3
from datetime import datetime, timezone
from email_alerts import send_email

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

    connection.execute("""
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            duration_seconds REAL,
            status TEXT NOT NULL
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


def update_incident(url, status):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, started_at
        FROM incidents
        WHERE url = ? AND status = 'OPEN'
        ORDER BY id DESC
        LIMIT 1
    """, (url,))

    incident = cursor.fetchone()

    if status == "DOWN" and incident is None:
        started_at = datetime.now(timezone.utc).isoformat()

        cursor.execute("""
            INSERT INTO incidents (url, started_at, status)
            VALUES (?, ?, 'OPEN')
        """, (url, started_at))

        connection.commit()

        print("New incident recorded!")

        send_email(
            "Website DOWN Alert",
            f"Alert! Your website is DOWN:\n\n{url}\n\nPlease check it."
        )

    elif status == "UP" and incident is not None:
        incident_id, started_at = incident

        ended_at = datetime.now(timezone.utc).isoformat()

        duration = (
            datetime.fromisoformat(ended_at)
            - datetime.fromisoformat(started_at)
        ).total_seconds()

        cursor.execute("""
            UPDATE incidents
            SET ended_at = ?,
                duration_seconds = ?,
                status = 'CLOSED'
            WHERE id = ?
        """, (ended_at, duration, incident_id))

        connection.commit()

        print("Incident closed!")

        send_email(
            "Website Recovery Alert",
            f"Good news! Your website is UP again:\n\n{url}\n\n"
            f"Total downtime: {duration:.2f} seconds."
        )

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

        update_incident(url, status)

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

        update_incident(url, "DOWN")


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

