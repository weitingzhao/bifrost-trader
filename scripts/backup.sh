#!/bin/bash
# Database backup script for Bifrost Trader

set -e

# Configuration
BACKUP_DIR="/backups"
DB_NAME=${DB_NAME:-bifrost_trader}
DB_USERNAME=${DB_USERNAME:-postgres}
DB_HOST=${DB_HOST:-postgres}
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
BACKUP_FILE="${BACKUP_DIR}/bifrost_trader_backup_${TIMESTAMP}.sql"
RETENTION_DAYS=${BACKUP_RETENTION_DAYS:-30}

echo "🔄 Starting database backup..."

# Create backup directory if it doesn't exist
mkdir -p ${BACKUP_DIR}

# Create database backup
echo "📊 Creating database backup: ${BACKUP_FILE}"
pg_dump -h ${DB_HOST} -U ${DB_USERNAME} -d ${DB_NAME} \
    --verbose \
    --clean \
    --if-exists \
    --create \
    --format=plain \
    --file=${BACKUP_FILE}

# Compress backup
echo "🗜️ Compressing backup..."
gzip ${BACKUP_FILE}
BACKUP_FILE="${BACKUP_FILE}.gz"

echo "✅ Backup created: ${BACKUP_FILE}"

# Clean up old backups
echo "🧹 Cleaning up old backups (older than ${RETENTION_DAYS} days)..."
find ${BACKUP_DIR} -name "bifrost_trader_backup_*.sql.gz" -type f -mtime +${RETENTION_DAYS} -delete

# List current backups
echo "📋 Current backups:"
ls -la ${BACKUP_DIR}/bifrost_trader_backup_*.sql.gz 2>/dev/null || echo "No backups found"

echo "🎉 Backup completed successfully!"
