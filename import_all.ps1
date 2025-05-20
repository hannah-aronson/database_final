Write-Host "📥 Importing title_basics.sql ..."
cmd /c "docker exec -i pg_autosteer psql -U autosteer -d autosteer_db < export/title_basics.sql"

Write-Host "📥 Importing title_principals.sql ..."
cmd /c "docker exec -i pg_autosteer psql -U autosteer -d autosteer_db < export/title_principals.sql"

Write-Host "📥 Importing name_basics.sql ..."
cmd /c "docker exec -i pg_autosteer psql -U autosteer -d autosteer_db < export/name_basics.sql"

Write-Host "✅ All data imported successfully (via PowerShell)."
