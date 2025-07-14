import datetime
import logging
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Setup logging
log_file = "/tmp/order_reminders_log.txt"
logging.basicConfig(filename=log_file, level=logging.INFO,
                    format='%(asctime)s - %(message)s')

# GraphQL endpoint
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=True,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate the date 7 days ago
seven_days_ago = (datetime.datetime.now() -
                  datetime.timedelta(days=7)).strftime("%Y-%m-%d")

# Define GraphQL query
query = gql(
    """
    query GetRecentOrders($since: Date!) {
        orders(orderDate_Gte: $since) {
            id
            customer {
                email
            }
        }
    }
    """
)

# Execute query
try:
    response = client.execute(query, variable_values={"since": seven_days_ago})
    orders = response.get("orders", [])

    for order in orders:
        order_id = order["id"]
        customer_email = order["customer"]["email"]
        logging.info(f"Order ID: {order_id}, Customer Email: {customer_email}")

    print("Order reminders processed!")

except Exception as e:
    logging.error(f"Error during GraphQL query: {e}")
    print("Failed to process order reminders.")
