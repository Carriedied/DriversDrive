# main.py

from scanner import find_problem_devices
from driver_search import search_driver_links_for_hwid
from downloader import download_for_device
from report import save_report
import os

def main():
    print("Сканирование устройств с проблемами...")
    devs = find_problem_devices()
    print(f"Найдено {len(devs)} устройств с ошибками.")

    results = []
    for dev in devs:
        print(f"Обработка устройства: {dev['name']} — HWIDs: {dev['hardware_ids']}")
        # Для каждого HWID пробуем поиск
        all_links = []
        for hw in dev["hardware_ids"]:
            links = search_driver_links_for_hwid(hw)
            all_links.extend(links)
            if links:
                break  # если уже нашли для одного HWID — остановим
        if not all_links:
            print("  => Не найдено ссылки на драйвер.")
        else:
            print(f"  => Найдено {len(all_links)} ссылок.")
        rec = download_for_device(dev, all_links)
        results.append(rec)
        if rec["downloaded"]:
            print("  => Успешно скачано:", rec["local_path"])
        else:
            print("  => Не удалось скачать драйвер.")
        print("-" * 40)

    # Сохраняем отчёт
    out = os.path.join("reports", "driver_report.json")
    save_report(out, results)

if __name__ == "__main__":
    main()
