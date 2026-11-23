
import sqlite3

DATABASE = "monitor.db"


def show_statistics():

    connection = sqlite3.connect(DATABASE)
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            url,
            COUNT(*),
            SUM(CASE WHEN status = 'UP' THEN 1 ELSE 0 END),
            SUM(CASE WHEN status = 'DOWN' THEN 1 ELSE 0 END),
            AVG(response_time)
        FROM monitoring_history
        GROUP BY url
    """)

    records = cursor.fetchall()

    print("\nWEBSITE UPTIME STATISTICS")
    print("=" * 55)

    for record in records:

        url, total, up, down, avg_response = record

        uptime = (up / total) * 100 if total else 0

        print(f"\nWebsite: {url}")
        print(f"Total Checks: {total}")
        print(f"Successful Checks: {up}")
        print(f"Failed Checks: {down}")
        print(f"Uptime: {uptime:.2f}%")
        print(f"Average Response: {avg_response:.2f} ms")

        print("-" * 55)

    connection.close()


if __name__ == "__main__":
    show_statistics()

