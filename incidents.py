
import sqlite3
from datetime import datetime, timezone

DATABASE = "monitor.db"


def show_incidents():
    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT id, url, started_at, ended_at,
               duration_seconds, status
        FROM incidents
        ORDER BY id DESC
    """)

    incidents = cursor.fetchall()

    print("\nWEBSITE INCIDENT REPORT")
    print("=" * 60)

    if not incidents:
        print("No incidents recorded yet.")

    for incident in incidents:
        incident_id, url, started, ended, duration, status = incident

        print(f"\nIncident ID: {incident_id}")
        print(f"Website: {url}")
        print(f"Started At: {started}")
        print(f"Status: {status}")

        if status == "OPEN":
            start_time = datetime.fromisoformat(started)
            duration = max(
                0,
                (datetime.now(timezone.utc) - start_time).total_seconds()
            )
            print(f"Current Downtime: {duration:.2f} seconds")
        else:
            print(f"Ended At: {ended}")
            print(f"Total Downtime: {duration:.2f} seconds")

        print("-" * 60)

    connection.close()


if __name__ == "__main__":
    show_incidents()
