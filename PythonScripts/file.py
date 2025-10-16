import wmi
import win32com.client

def get_computers_from_ad():
    ad = win32com.client.GetObject('LDAP://rootDSE')
    domain = ad.Get('defaultNamingContext')
    searcher = win32com.client.Dispatch("ADsDSOObject")
    query = f"<LDAP://{domain}>;(objectClass=computer);name;subtree"
    rs, _ = searcher.ExecuteSearch(query)
    computers = []
    while True:
        item = rs.GetNext()
        if not item:
            break
        name = item.Properties("name").Value
        computers.append(name)
    rs.Close()
    return computers

def check_remote_devices(host):
    try:
        conn = wmi.WMI(computer=host)
        print(f"--- {host} ---")
        for device in conn.Win32_PnPEntity():
            if device.ConfigManagerErrorCode != 0:
                print(f"{device.Name} — ошибка: {device.ConfigManagerErrorCode}")
        print()
    except Exception as e:
        print(f"Не удалось подключиться к {host}: {e}")

if __name__ == "__main__":
    computers = get_computers_from_ad()
    for comp in computers:
        check_remote_devices(comp)
