
import httpx
import time
import sqlite3
import os
from datetime import datetime, timezone
from email_alerts import send_email

WEBSITES = [
    "https://google.com",
    "https://github.com",
    "https://microsoft.com"
]

DATABASE = "/app/data/monitor.db"

RESPONSE_TIME_THRESHOLD = 2000


def create_database():
    os.makedirs(os.path.dirname(DATABASE), exist_ok=True)

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

    connection.execute("""
        CREATE TABLE IF NOT EXISTS performance_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            started_at TEXT NOT NULL,
            ended_at TEXT,
            max_response_time REAL,
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
        print("New incident recorded!", flush=True)

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
        print("Incident closed!", flush=True)

        send_email(
            "Website Recovery Alert",
            f"Good news! Your website is UP again:\n\n{url}\n\n"
            f"Total downtime: {duration:.2f} seconds."
        )

    connection.close()


def update_performance_incident(url, response_time):
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, started_at, max_response_time
        FROM performance_incidents
        WHERE url = ? AND status = 'OPEN'
        ORDER BY id DESC
        LIMIT 1
    """, (url,))

    incident = cursor.fetchone()

    if response_time > RESPONSE_TIME_THRESHOLD:

        if incident is None:
            started_at = datetime.now(timezone.utc).isoformat()

            cursor.execute("""
                INSERT INTO performance_incidents
                (url, started_at, max_response_time, status)
                VALUES (?, ?, ?, 'OPEN')
            """, (url, started_at, response_time))

            connection.commit()
            print("Performance threshold exceeded!", flush=True)

            send_email(
                "Website Slow Performance Alert",
                f"Warning! Website response time is too high.\n\n"
                f"Website: {url}\n"
                f"Response Time: {response_time:.2f} ms\n"
                f"Allowed Threshold: {RESPONSE_TIME_THRESHOLD} ms"
            )

        else:
            incident_id, started_at, max_response_time = incident

            if response_time > max_response_time:
                cursor.execute("""
                    UPDATE performance_incidents
                    SET max_response_time = ?
                    WHERE id = ?
                """, (response_time, incident_id))

                connection.commit()

            print(
                "Website is still above performance threshold.",
                flush=True
            )

    elif incident is not None:
        incident_id, started_at, max_response_time = incident
        ended_at = datetime.now(timezone.utc).isoformat()

        cursor.execute("""
            UPDATE performance_incidents
            SET ended_at = ?,
                status = 'CLOSED'
            WHERE id = ?
        """, (ended_at, incident_id))

        connection.commit()
        print("Website performance recovered!", flush=True)

        send_email(
            "Website Performance Recovery Alert",
            f"Good news! Website performance has recovered.\n\n"
            f"Website: {url}\n"
            f"Current Response Time: {response_time:.2f} ms\n"
            f"Maximum Response Time: {max_response_time:.2f} ms"
        )

    connection.close()


def check_website(url):
    print(f"\nChecking: {url}", flush=True)
    start = time.perf_counter()

    try:
        response = httpx.get(
            url,
            timeout=10,
            follow_redirects=True
        )

        response_time = (time.perf_counter() - start) * 1000
        status = "UP" if 200 <= response.status_code < 400 else "DOWN"

        print(f"Status: {status}", flush=True)
        print(f"HTTP Code: {response.status_code}", flush=True)
        print(f"Response Time: {response_time:.2f} ms", flush=True)

        save_result(
            url,
            status,
            response.status_code,
            response_time
        )

        update_incident(url, status)

        if status == "UP":
            update_performance_incident(url, response_time)

    except httpx.RequestError as error:
        response_time = (time.perf_counter() - start) * 1000

        print("Status: DOWN", flush=True)
        print(f"Error: {error}", flush=True)

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

    print("WEBSITE HEALTH & UPTIME MONITOR", flush=True)
    print("Database connected successfully!", flush=True)
    print(
        f"Performance Threshold: {RESPONSE_TIME_THRESHOLD} ms",
        flush=True
    )

    while True:
        print("\nStarting monitoring cycle...", flush=True)

        for website in WEBSITES:
            check_website(website)

        print("\nAll results saved to database.", flush=True)
        print("Next check in 60 seconds...", flush=True)

        time.sleep(60)

