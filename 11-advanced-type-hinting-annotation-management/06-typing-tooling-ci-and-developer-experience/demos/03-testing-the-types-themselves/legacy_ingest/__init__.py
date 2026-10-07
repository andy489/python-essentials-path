def fetch_batch(source):
    records = []
    with open(source, encoding="utf-8") as handle:
        for line in handle:
            line = line.strip()
            if not line:
                continue
            device_id, temperature, status, timestamp = line.split(",")
            records.append(
                {
                    "device_id": device_id,
                    "temperature": float(temperature),
                    "status": status,
                    "timestamp": timestamp,
                }
            )
    return records
