import pandas as pd
from sqlalchemy import create_engine, text
from tqdm import tqdm
import gc
from config import DB_CONFIG

def get_engine():
    url = f'postgresql+psycopg2://{DB_CONFIG["user"]}:{DB_CONFIG["password"]}@{DB_CONFIG["host"]}:{DB_CONFIG["port"]}/{DB_CONFIG["dbname"]}'
    return create_engine(url)

def table_exists(engine, table_name):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_schema = 'public' AND table_name = :table_name
            )
        """), {"table_name": table_name})
        return result.scalar()

def get_table_count(engine, table_name):
    with engine.connect() as conn:
        result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
        return result.scalar()

def import_table(filename: str, table_name: str, converters=None, chunksize=10000):
    print(f"📥 準備匯入 {filename} 到 {table_name} ...")
    engine = get_engine()

    first = True
    reader = pd.read_csv(filename, sep="\t", dtype=str, na_values="\\N", chunksize=chunksize)
    
    for chunk in tqdm(reader, desc=f"⏳ 匯入 {table_name}", unit="chunk"):
        if converters:
            for col, func in converters.items():
                if col in chunk:
                    chunk[col] = func(chunk[col])
        chunk.to_sql(table_name, engine, if_exists="replace" if first else "append", index=False)
        first = False
        del chunk
        gc.collect()

    print(f"✅ 完成匯入：{table_name}")
    final_count = get_table_count(engine, table_name)
    print(f"📊 匯入後 {table_name} 總資料數：{final_count} 筆\n")

def main_import_all():
    engine = get_engine()

    table_jobs = [
        ("title.basics.tsv", "title_basics", {
            "isAdult": lambda col: col.fillna("0").astype(int).astype(bool),
            "startYear": lambda col: pd.to_numeric(col, errors="coerce"),
            "endYear": lambda col: pd.to_numeric(col, errors="coerce"),
            "runtimeMinutes": lambda col: pd.to_numeric(col, errors="coerce"),
        }),
        ("title.principals.tsv", "title_principals", {
            "ordering": lambda col: pd.to_numeric(col, errors="coerce")
        }),
        ("name.basics.tsv", "name_basics", {
            "birthYear": lambda col: pd.to_numeric(col, errors="coerce"),
            "deathYear": lambda col: pd.to_numeric(col, errors="coerce"),
        }),
    ]

    for filename, table_name, converters in table_jobs:
        print(f"\n==== 處理資料表 {table_name} ====")
        if table_exists(engine, table_name):
            count = get_table_count(engine, table_name)
            print(f"⚠️ 資料表 {table_name} 已存在，已有 {count} 筆資料，跳過匯入。")
        else:
            import_table(filename, table_name, converters)

if __name__ == "__main__":
    main_import_all()

