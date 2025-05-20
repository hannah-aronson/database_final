#!/bin/bash

echo "📥 Importing title_basics..."
psql -U autosteer -h localhost -d autosteer_db < export/title_basics.sql

echo "📥 Importing title_principals..."
psql -U autosteer -h localhost -d autosteer_db < export/title_principals.sql

echo "📥 Importing name_basics..."
psql -U autosteer -h localhost -d autosteer_db < export/name_basics.sql

echo "✅ All tables imported."
