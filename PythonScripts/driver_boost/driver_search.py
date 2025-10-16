# driver_search.py

import requests
from urllib.parse import quote
from config import MS_CATALOG_SEARCH_URL

def build_search_url(hwid: str):
    """
    Формирует URL поискового запроса в Microsoft Catalog Update.
    Например, можно просто вставить hwid в query string.
    """
    q = quote(hwid)
    return f"{MS_CATALOG_SEARCH_URL}{q}"

def search_driver_links_for_hwid(hwid: str):
    """
    Пытается найти ссылки на драйверы для данного hardware-id.
    Возвращает список dict:
      {"link": URL, "title": str}
    (упрощённо — парсинг HTML каталога)
    """
    url = build_search_url(hwid)
    resp = requests.get(url, timeout=10)
    if resp.status_code != 200:
        return []
    html = resp.text

    # **Простой парсинг** — искать <a href="...">Download</a> или похожее.
    # Это очень хрупко и зависит от структуры страницы Microsoft Catalog.
    links = []
    # пример: ищем “href="/DownloadDialog.aspx?…” в html
    import re
    pattern = re.compile(r'<a href="(/DownloadDialog\.aspx\?[^"]+)"[^>]*>([^<]+)</a>', re.IGNORECASE)
    for match in pattern.finditer(html):
        rel = match.group(1)
        title = match.group(2)
        full = "https://www.catalog.update.microsoft.com" + rel
        links.append({"link": full, "title": title})
    return links
