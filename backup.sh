#!/bin/bash

# Source the .env file to get the environment variables
source whatsfeed_app/.env

# Use mysqldump to dump the database
mysqldump -h $HOST -u $USER -p$PASSWORD $DATABASE >backups/whatsfeed_db_backup_$(date +%4Y-%m-%d_%H:%M:%S).sql