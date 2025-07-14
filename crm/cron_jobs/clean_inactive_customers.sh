#!/bin/bash

# Get directory of current script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Change to project root (assumes script is at crm/cron_jobs/)
cd "$SCRIPT_DIR/../.."

# Store current working directory
CWD=$(pwd)

# Timestamp and log file
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
LOG_FILE="/tmp/customer_cleanup_log.txt"

# Ensure we're in the correct directory
if [ -f "manage.py" ]; then
  DELETED_COUNT=$(python manage.py shell <<EOF
from datetime import timedelta
from django.utils import timezone
from crm.models import Customer

cutoff = timezone.now() - timedelta(days=365)
qs = Customer.objects.filter(order__isnull=True, created_at__lt=cutoff)
count = qs.count()
qs.delete()
print(count)
EOF
  )

  echo "$TIMESTAMP - Deleted $DELETED_COUNT inactive customers" >> "$LOG_FILE"
else
  echo "$TIMESTAMP - ERROR: manage.py not found in cwd ($CWD)" >> "$LOG_FILE"
fi
