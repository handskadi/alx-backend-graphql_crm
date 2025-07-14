from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    # Log the timestamp to file
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    message = f"{timestamp} CRM is alive"

    with open("/tmp/crm_heartbeat_log.txt", "a") as f:
        f.write(message + "\n")

    # GraphQL ping using gql
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("{ hello }")
        result = client.execute(query)
        print("GraphQL hello response:", result.get("hello", "No response"))

    except Exception as e:
        print(f"GraphQL query failed: {e}")

def update_low_stock():
    timestamp = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        mutation = gql("""
        mutation {
            updateLowStockProducts {
                updatedProducts
                message
            }
        }
        """)

        result = client.execute(mutation)
        updates = result['updateLowStockProducts']['updatedProducts']
        message = result['updateLowStockProducts']['message']

        with open("/tmp/low_stock_updates_log.txt", "a") as f:
            f.write(f"{timestamp} - {message}\n")
            for item in updates:
                f.write(f"{timestamp} - Updated: {item}\n")

        print("Low stock update cron executed.")

    except Exception as e:
        print(f"Low stock cron error: {e}")
