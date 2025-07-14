from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql',
            verify=False,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)

        query = gql("""
        query {
            totalCustomers
            totalOrders
            totalRevenue
        }
        """)

        result = client.execute(query)
        customers = result['totalCustomers']
        orders = result['totalOrders']
        revenue = result['totalRevenue']

        with open("/tmp/crm_report_log.txt", "a") as f:
            f.write(f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")

    except Exception as e:
        print(f"Failed to generate CRM report: {e}")
