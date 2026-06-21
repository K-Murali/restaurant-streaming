from dotenv import load_dotenv
import os
from azure.eventhub import EventHubProducerClient
from azure.eventhub.exceptions import AuthenticationError

load_dotenv("00_synthetic_data/.env")

conn_str = os.getenv("EVENTHUB_CONNECTION_STRING")
eh_name = os.getenv("EVENTHUB_NAME")

print("Testing Event Hub authentication...")
if not conn_str or not eh_name:
    print("Missing EVENTHUB_CONNECTION_STRING or EVENTHUB_NAME in .env")
    raise SystemExit(1)

try:
    producer = EventHubProducerClient.from_connection_string(conn_str, eventhub_name=eh_name)
    # attempt to create a batch (this opens connection and validates auth)
    batch = producer.create_batch()
    producer.close()
    print("Authentication OK: connected to Event Hub", eh_name)
except AuthenticationError as e:
    print("Authentication failed:")
    print(e)
    raise
except Exception as e:
    print("Unexpected error while testing authentication:")
    print(e)
    raise
