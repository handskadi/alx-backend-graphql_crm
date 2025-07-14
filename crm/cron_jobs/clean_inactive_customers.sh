#!/bin/bash

# Resolve the absolute path of the current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
echo "Changing to project root from cwd: $SCRIPT_DIR"

# Move to the root of the Django project (adjust if needed)
cd "$SCRIPT_DIR/../.." || {
    echo "Failed to change directory to project root"
    exit 1
}

# Run the Django cleanup using manage.py shell
DELETED_COUNT=$(python3 manage.py shell << END
from crm.models import Customer
from django.utils import timezone
from datetime import timedelta

cutoff = timezone.now() - timedelta(days=365)
deleted, _ = Customer.objects.filter(last_order_date__lt=cutoff).delete()
print(deleted)
END
)

# Log with timestamp
if [ -n "$DELETED_COUNT" ]; then
    echo "$(date): Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt
else
    echo "$(date): No customers deleted" >> /tmp/customer_cleanup_log.txt
fi
