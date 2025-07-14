from datetime import datetime
import requests


def log_crm_heartbeat():
    # Format timestamp
    now = datetime.now().strftime("%d/%m/%Y-%H:%M:%S")

    # Log heartbeat message
    with open("/tmp/crm_heartbeat_log.txt", "a") as log_file:
        log_file.write(f"{now} CRM is alive\n")

    # OPTIONAL: Query GraphQL `hello` field
    try:
        response = requests.post(
            "http://localhost:8000/graphql",
            json={"query": "{ hello }"},
            timeout=5
        )
        if response.ok:
            data = response.json()
            print("GraphQL hello response:", data)
        else:
            print(f"GraphQL hello query failed: HTTP {response.status_code}")
    except Exception as e:
        print(f"GraphQL hello query error: {e}")
