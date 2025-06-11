DB_CONFIG = {
    "dbname": "autosteer_db",
    "user": "autosteer",
    "password": "autosteer_database",
    "host": "localhost",
    "port": "5432"
}

QUERY_DEFAULT = """
SELECT 
    n."primaryName",
    COUNT(*) AS total_movies
FROM name_basics n
JOIN title_principals p ON n.nconst = p.nconst
GROUP BY n."primaryName"
HAVING COUNT(*) > 50
ORDER BY total_movies DESC
LIMIT 50;
"""
