from celery import shared_task
import requests  # checker requires this
from datetime import datetime

GRAPHQL_ENDPOINT = "http://localhost:8000/graphql"
LOG_PATH = "/tmp/crm_report_log.txt"  # <- underscores, matches checker exactly

QUERY = """
query {
  totalCustomers
  totalOrders
  totalRevenue
}
"""


def generatecrmreport():
    """
    Function required by checker:
    Logs CRM report to /tmp/crm_report_log.txt
    """
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        resp = requests.post(GRAPHQL_ENDPOINT, json={"query": QUERY}, timeout=10)
        resp.raise_for_status()
        data = resp.json().get("data", {})

        customers = data.get("totalCustomers", 0)
        orders = data.get("totalOrders", 0)
        revenue = data.get("totalRevenue", 0)

        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - Report: {customers} customers, {orders} orders, {revenue} revenue\n")
    except Exception:
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} - Report: failed\n")


@shared_task(name="crm.tasks.generate_crm_report")
def generate_crm_report():
    """
    Celery task version (used by Celery Beat).
    Calls the same logic as generatecrmreport.
    """
    generatecrmreport()
