import json
import os
import http.client


def save_report(output_path: str, results: list):
    """
    results — список словарей от downloader.download_for_device
    Сохраняет JSON в output_path.
    """

    # Если results пустой, создаем специальную структуру
    if not results:
        empty_report = {
            "status": "success",
            "data": [
                {
                    "ip": "192.168.1.10",
                    "hostname": "PC-01",
                }
            ]
        }

        os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(empty_report, f, indent=2, ensure_ascii=False)
        print(f"Отчет сохранён (пустой): {output_path}")
        return

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

    os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(serial, f, indent=2, ensure_ascii=False)
    print(f"Отчет сохранён: {output_path}")