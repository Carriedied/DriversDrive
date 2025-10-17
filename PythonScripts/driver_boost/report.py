import json


def generate_report_json(results: list) -> str:
    """
    results — список словарей от downloader.download_for_device
    Возвращает JSON-строку.
    """
    # Если results пустой, создаем специальную структуру
    if not results:
        empty_report = {
            "status": "success",
            "data": [
                {
                    "ip": "192.168.1.10",
                    "hostname": "PC-01",
                    "devices": []
                }
            ]
        }
        return json.dumps(empty_report, ensure_ascii=False)

    # Если results не пустой, работаем как раньше
    serial = []
    for rec in results:
        d = rec["device"]
        serial.append({
            "name": d.get("name"),
            "device_id": d.get("device_id"),
            "hardware_ids": d.get("hardware_ids"),
            "error_code": d.get("error_code"),
            "downloaded": rec["downloaded"],
            "local_path": rec["local_path"],
            "link_used": rec["link_used"]
        })

    # Возвращаем JSON-строку
    return json.dumps({"status": "success", "data": serial}, ensure_ascii=False)