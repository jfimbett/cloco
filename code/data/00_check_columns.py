"""Quick schema check — run once to find actual column names in WRDS tables."""
import wrds
db = wrds.Connection(wrds_username="juanimbet")

for lib, tbl in [("comp", "company"), ("comp", "names")]:
    print(f"\n=== {lib}.{tbl} columns ===")
    cols = db.describe_table(lib, tbl)
    print(cols[["name", "type"]].to_string())

db.close()
