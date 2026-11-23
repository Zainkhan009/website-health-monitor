
from monitor import create_database, update_incident

TEST_URL = "https://test-incident.example.com"

create_database()

print("\nTesting DOWN alert...")
update_incident(TEST_URL, "DOWN")

print("\nTesting UP recovery alert...")
update_incident(TEST_URL, "UP")

print("\nEmail alert test completed!")
