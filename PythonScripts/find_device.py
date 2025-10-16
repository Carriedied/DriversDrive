import wmi, ipaddress

def check_missing_drivers():
    c = wmi.WMI()
    print("Устройства без драйвера:\n")

    for device in c.Win32_PnPEntity():
        if device.ConfigManagerErrorCode != 0:
            print(f"{device.Name} (Ошибка: {device.ConfigManagerErrorCode})")
            print(f"DeviceID: {device.DeviceID}")
            print("-" * 50)

if __name__ == "__main__":
    check_missing_drivers()
    # print(ipaddress.ip_address())
