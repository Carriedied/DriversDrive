import sys
import json
import os
import traceback

# --- Импорты из ваших скриптов ---
try:
    from scanner import find_problem_devices
    from driver_search import search_driver_links_for_hwid
    from downloader import download_for_device
except ImportError as e:
    print(json.dumps({"status": "error", "error": f"Ошибка импорта модуля: {e}"}))
    sys.exit(1)

# --- Основная логика из main.py, адаптированная ---
def run_driver_scan_and_download_logic():
    """
    Выполняет основную логику сканирования, поиска и скачивания.
    Возвращает результат в формате, подходящем для JSON.
    """
    # print("Сканирование устройств с проблемами...", file=sys.stderr)  # УБРАТЬ
    devs = find_problem_devices()
    # print(f"Найдено {len(devs)} устройств с ошибками.", file=sys.stderr)  # УБРАТЬ

    results = []
    for dev in devs:
        # print(f"Обработка устройства: {dev['name']} — HWIDs: {dev['hardware_ids']}", file=sys.stderr)  # УБРАТЬ
        # Для каждого HWID пробуем поиск
        all_links = []
        for hw in dev["hardware_ids"]:
            links = search_driver_links_for_hwid(hw)
            all_links.extend(links)
            if links:
                break  # если уже нашли для одного HWID — остановим
        # if not all_links:
        #     print("  => Не найдено ссылки на драйвер.", file=sys.stderr)  # УБРАТЬ
        # else:
        #     print(f"  => Найдено {len(all_links)} ссылок.", file=sys.stderr)  # УБРАТЬ
        rec = download_for_device(dev, all_links)
        results.append(rec)
        # if rec["downloaded"]:
        #     print("  => Успешно скачано:", rec["local_path"], file=sys.stderr)  # УБРАТЬ
        # else:
        #     print("  => Не удалось скачать драйвер.", file=sys.stderr)  # УБРАТЬ
        # print("-" * 40, file=sys.stderr)  # УБРАТЬ

    # Формируем JSON-результат в нужном формате для C#
    devices_list = []
    for rec in results:
        d = rec["device"]
        status = "up-to-date"
        url = ""

        if not rec["downloaded"]:
            if rec["link_used"]:
                status = "missing"
                url = rec["link_used"]
            else:
                status = "outdated"  # или "missing", если ссылка не найдена
        else:
            status = "up-to-date"

        devices_list.append({
            "name": d.get("name", "Unknown Device"),
            "driver_status": status,
            "driver_url": url
        })

    # Возвращаем в формате Computer (один компьютер — текущий)
    computer_data = {
        "ip": "127.0.0.1",  # или получите реальный IP, если нужно
        "hostname": os.environ.get('COMPUTERNAME', 'localhost'),
        "devices": devices_list
    }

    return [computer_data]  # Возвращаем список компьютеров (в данном случае один)

# --- Основная функция для обработки stdin/stdout ---
def main_api():
    """
    Читает JSON-запрос из stdin, выполняет команду, выводит JSON-ответ в stdout.
    """
    # Читаем ввод
    input_data = sys.stdin.read().strip()
    sys.stdin.close()

    if not input_data:
        print(json.dumps({"status": "error", "error": "Пустой ввод"}))
        return

    try:
        request = json.loads(input_data)
    except json.JSONDecodeError:
        print(json.dumps({"status": "error", "error": "Неверный JSON"}))
        return

    command = request.get("command")

    if command == "run_driver_scan_and_download":
        try:
            # Выполняем основную логику
            scan_and_download_results = run_driver_scan_and_download_logic()

            # Формируем успешный ответ с данными
            result = {"status": "success", "data": scan_and_download_results}
        except Exception as e:
            # Обработка ошибок при выполнении основной логики
            error_message = str(e)
            # detailed_error = traceback.format_exc() # Для отладки в stderr
            # print(f"Ошибка выполнения логики: {detailed_error}", file=sys.stderr)  # УБРАТЬ
            result = {"status": "error", "error": error_message}
    else:
        # Неизвестная команда
        result = {"status": "error", "error": f"Неизвестная команда: {command}"}

    # Выводим JSON-ответ в stdout
    print(json.dumps(result))

if __name__ == "__main__":
    main_api()