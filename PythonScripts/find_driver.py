import wmi

def list_devices():
    c = wmi.WMI()
    print("Список устройств:\n")

    for device in c.Win32_PnPEntity():
        status = device.Status or "Unknown"
        name = device.Name or "No name"
        device_id = device.DeviceID or "-"
        driver = "No driver info"

        print(f"Устройство: {name}")
        print(f"  Статус: {status}")
        print(f"  Device ID: {device_id}")
        print(f"  Версия драйвера: {driver}")
        print("-" * 60)

if __name__ == "__main__":
    list_devices()
