
import sqlite3

DATABASE = "monitor.db"


def show_history():
    connection = sqlite3.connect(DATABASE)

    cursor = connection.cursor()

    cursor.execute("""
        SELECT url, status, status_code, response_time, checked_at
        FROM monitoring_history
        ORDER BY id DESC
        LIMIT 20
    """)

    records = cursor.fetchall()

    print("\nWEBSITE MONITORING HISTORY")
    print("=" * 80)

    for record in records:
        url, status, code, response_time, checked_at = record

        print(f"\nWebsite: {url}")
        print(f"Status: {status}")
        print(f"HTTP Code: {code}")
        print(f"Response Time: {response_time:.2f} ms")
        print(f"Checked At: {checked_at}")
        print("-" * 50)

    connection.close()


if __name__ == "__main__":
    show_history()
