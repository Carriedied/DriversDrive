# scanner.py

import wmi

def find_problem_devices():
    """
    Возвращает список устройств с ошибками / без драйверов.
    Каждое устройство — dict с минимум:
      - name
      - device_id
      - hardware_ids (список)
      - error_code (ConfigManagerErrorCode)
    """
    c = wmi.WMI()
    result = []
    for dev in c.Win32_PnPEntity():
        code = dev.ConfigManagerErrorCode
        if code is None:
            continue
        if code != 0:
            name = dev.Name or ""
            device_id = dev.DeviceID or ""
            # Hardware IDs могут быть в свойстве PNPDeviceID или через Win32_PnPEntity’s data
            hwids = []
            try:
                hwids = dev.HardwareID  # может быть список или None
            except Exception:
                hwids = []
            # Приводим к списку строк
            hwids = hwids if isinstance(hwids, (list, tuple)) else ([hwids] if hwids else [])
            result.append({
                "name": name,
                "device_id": device_id,
                "hardware_ids": hwids,
                "error_code": code
            })
    return result
