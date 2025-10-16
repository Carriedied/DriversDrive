# downloader.py

import os
import requests
from config import DRIVER_DOWNLOAD_FOLDER, MAX_DOWNLOAD_TRIES

def ensure_folder():
    if not os.path.exists(DRIVER_DOWNLOAD_FOLDER):
        os.makedirs(DRIVER_DOWNLOAD_FOLDER, exist_ok=True)

def download_file(url: str, filename: str):
    """
    Скачивает файл по URL в DRIVER_DOWNLOAD_FOLDER с именем filename.
    Возвращает локальный путь или None при ошибке.
    """
    ensure_folder()
    target = os.path.join(DRIVER_DOWNLOAD_FOLDER, filename)
    tries = 0
    while tries < MAX_DOWNLOAD_TRIES:
        try:
            resp = requests.get(url, timeout=15)
            if resp.status_code == 200:
                with open(target, "wb") as f:
                    f.write(resp.content)
                return target
            else:
                tries += 1
        except Exception as e:
            tries += 1
    return None

def download_for_device(device_info: dict, driver_links: list):
    """
    Для одного устройства + найденных ссылок драйверов:
    скачивает (первую) и возвращает статус.
    Возвращает dict:
      {
        "device": device_info,
        "downloaded": True/False,
        "local_path": ...,  # если скачано
        "link_used": ...    # ссылка, по которой скачали
      }
    """
    for dl in driver_links:
        link = dl.get("link")
        title = dl.get("title", "")
        # можно попытаться выбрать файл из title или добавить расширение
        fname = title
        if not fname:
            # fallback: взять часть URL
            fname = link.split("/")[-1]
        local = download_file(link, fname)
        if local:
            return {
                "device": device_info,
                "downloaded": True,
                "local_path": local,
                "link_used": link
            }
    # ни один не скачан
    return {
        "device": device_info,
        "downloaded": False,
        "local_path": None,
        "link_used": None
    }
