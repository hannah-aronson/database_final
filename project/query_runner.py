import psycopg2
from config import DB_CONFIG, QUERY_DEFAULT

_last_hint_applied = None

def reset_hint_cache():
    global _last_hint_applied
    _last_hint_applied = None

def apply_hint_indexes(hint: str):
    global _last_hint_applied

    # ✅ 若連續呼叫相同 hint，就跳過 index 操作
    if _last_hint_applied == hint:
        print(f"↪️  Skipping re-apply (Hint {hint} already applied)")
        return

    _last_hint_applied = hint  # 更新快取

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    if hint == 'A':
        cur.execute('CREATE INDEX IF NOT EXISTS idx_name_primaryName ON name_basics("primaryName");')
        cur.execute("CREATE INDEX IF NOT EXISTS idx_principal_nconst ON title_principals(nconst);")
        cur.execute('CREATE INDEX IF NOT EXISTS idx_title_primaryTitle ON title_basics("primaryTitle");')

    elif hint == 'B':
        cur.execute('CREATE INDEX IF NOT EXISTS idx_title_startYear ON title_basics("startYear");')
        cur.execute('CREATE INDEX IF NOT EXISTS idx_title_type ON title_basics("titleType");')

    elif hint == 'C':
        cur.execute("DROP INDEX IF EXISTS idx_name_primaryName;")
        cur.execute("DROP INDEX IF EXISTS idx_principal_nconst;")
        cur.execute("DROP INDEX IF EXISTS idx_title_startYear;")
        cur.execute("DROP INDEX IF EXISTS idx_title_type;")
        cur.execute("DROP INDEX IF EXISTS idx_title_primaryTitle;")

    print(f"✅ Applied Hint {hint}")
    conn.commit()
    conn.close()


def run_query(query: str = QUERY_DEFAULT) -> float:
    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()
    import time
    start = time.time()
    cur.execute(query)
    cur.fetchall()
    end = time.time()
    conn.close()
    return (end - start) * 1000  # latency in ms