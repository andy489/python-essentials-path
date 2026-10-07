from typing import reveal_type

from legacy_ingest import fetch_batch

batch = fetch_batch("legacy.csv")
reveal_type(batch)
record = batch[0]
print(record.strip())
