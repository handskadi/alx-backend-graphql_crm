#!/usr/bin/env python3

import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

import os
from datetime import datetime as dt

# Setup GraphQL client
transport = RequestsHTTPTransport(
    url="http://localhost:8000/graphql",
    verify=False,
    retries=3,
)

client = Client(transport=transport, fetch_schema_from_transport=True)

# Calculate 7 days ago
seven_days_ago = (dt.now() - datetime.timedelta(days=7)).date()

# GraphQL query
query = gql(f"""
query {{
  orders(orderDate_Gte: "{seven_days_ago}") {{
    id
    customer {{
      email
    }}
  }}
}}
""")

try:
    response = client.execute(query)
    orders = response.get("orders", [])

    with open("/tmp/order_reminders_log.txt", "a") as log_file:
        timestamp = dt.now().strftime("%Y-%m-%d %H:%M:%S")
        for order in orders:
            log_file.write(f"{timestamp} - Order ID: {order['id']}, Email: {order['customer']['email']}\n")

    print("Order reminders processed!")

except Exception as e:
    print(f"Error while processing reminders: {e}")
