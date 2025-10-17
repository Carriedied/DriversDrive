DriverDrive — Централизованное управление драйверами в локальной сети

Кейс "Драйверный Драйв" — хакатон "Кодовые Границы: Драйв и Прорыв 2025"

Описание задачи

Разработка решения для централизованного развертывания драйверов на устройствах в локальной сети с одного компьютера.  
Решение должно обеспечить упрощение процесса обновления и установки драйверов, минимизируя время и усилия, затрачиваемые на обслуживание компьютерной инфраструктуры.

Архитектура

Проект состоит из двух основных частей:

C# WPF приложение — пользовательский интерфейс (UI), реализованный по паттерну MVVM.
Python скрипты — логика сканирования сети, поиска устройств и драйверов, установки драйверов.

Связь между C# и Python осуществляется через межпроцессное взаимодействие (IPC) с использованием JSON и стандартных потоков (stdin/stdout).

C# WPF Приложение (DriverDrive.App)

Назначение
Предоставляет пользователю графический интерфейс для:
Сканирования локальной сети.
Просмотра устройств с проблемами (отсутствующие или устаревшие драйверы).
Установки драйверов на удалённые устройства.

Структура проекта

DriverDrive/
├── DriverDrive.Core/          # Ядро: модели, сервисы, интерфейсы
├── DriverDrive.Infrastructure/ # Внешние зависимости: PythonExecutorService
├── DriverDrive.ViewModel/      # Логика UI: MainViewModel, RelayCommand
├── DriverDrive.View/           # Представление: XAML, конвертеры
└── DriverDrive.App/            # Точка входа: App.xaml, MainWindow.xaml

Ключевые компоненты

MainViewModel.cs
Реализует логику сканирования и установки драйверов.
Использует IDeviceScannerService и IDriverInstallerService.
Обрабатывает команды ScanCommand и InstallDriverCommand.

PythonExecutorService.cs
Реализует IDeviceScannerService и IDriverInstallerService.
Запускает Python-скрипт, отправляет JSON-запрос, получает JSON-ответ.
Использует Process для IPC.

MainWindow.xaml
Отображает список компьютеров и устройств.
Использует ListView, DataTemplate, IValueConverter для отображения статуса драйвера.
Современный дизайн с карточками, кнопками, тенями.

RelayCommand.cs
Реализация ICommand с поддержкой асинхронности.
Используется для привязки команд к кнопкам.

Python Скрипты

Назначение
Выполняют системные операции:
Сканирование устройств в локальной сети.
Поиск драйверов для устройств.
Установка драйверов на удалённые устройства.

Структура

PythonScripts/
└── driver_boost/
    ├── driver_manager_api.py   # Главный API: принимает команды, вызывает другие модули
    ├── scanner.py              # Сканирование устройств с ошибками
    ├── driver_search.py        # Поиск ссылок на драйверы по HWID
    ├── downloader.py           # Скачивание драйверов
    └── report.py               # Формирование отчёта (не используется напрямую)

Ключевые функции

driver_manager_api.py
Принимает JSON-запрос из C#.
Выполняет команду run_driver_scan_and_download.
Возвращает JSON-ответ с данными о устройствах и драйверах.

scanner.py
Использует wmi для получения информации о устройствах.
Находит устройства с ошибками (например, ERROR_CODE != 0).

driver_search.py
Ищет ссылки на драйверы по HWID с помощью requests и BeautifulSoup.

downloader.py
Скачивает драйверы по найденным ссылкам.
Сохраняет их локально.

Как это работает

Пользователь нажимает "Сканировать сеть".
MainViewModel вызывает IDeviceScannerService.ScanNetworkAsync().
PythonExecutorService запускает driver_manager_api.py и отправляет JSON-запрос:
{
  "command": "run_driver_scan_and_download",
  "params": {}
}
Python-скрипт выполняет сканирование, поиск и скачивание драйверов.
Python возвращает JSON-ответ:
{
  "status": "success",
  "data": [
    {
      "ip": "192.168.1.10",
      "hostname": "PC-01",
      "devices": [
        {
          "name": "NVIDIA GeForce RTX 3060",
          "driver_status": "missing",
          "driver_url": "https://example.com/driver.exe"
        }
      ]
    }
  ]
}
PythonExecutorService десериализует ответ и передаёт данные в MainViewModel.
MainWindow отображает данные в виде списка устройств.

Установка и запуск

Требования

Windows 10/11
.NET 8.0 Runtime (или SDK)
Python 3.8+
Зависимости Python: pip install wmi requests beautifulsoup4 pywin32 psutil lxml

Запуск

Склонируйте репозиторий:
git clone https://github.com/yourusername/DriversDrive.git
cd DriversDrive

Установите Python-зависимости:
cd PythonScripts/driver_boost
pip install -r requirements.txt

Откройте решение в Visual Studio:
Откройте DriverDrive.sln.
Убедитесь, что все проекты используют .NET 8.0-windows.

Запустите приложение:
Нажмите F5 в Visual Studio.
Или запустите через dotnet run:
cd DriverDrive.App
dotnet run

Возможные ошибки при запуске

Если при запуске возникает сообщение вида:

You must install or update .NET to run this application.
App: d:\Users\user\Desktop\DriversDrive-main\DriverDrive.App\bin\Debug\net8.0-windows\DriverDrive.App.exe
Architecture: x64
Framework: 'Microsoft.WindowsDesktop.App', version '8.0.0' (x64)
.NET location: C:\Program Files\dotnet\

The following frameworks were found:
  6.0.1 at [C:\Program Files\dotnet\shared\Microsoft.WindowsDesktop.App]

Это означает, что требуемая версия .NET (в данном примере — 8.0.0) не установлена.
Решение:
Установите .NET Desktop Runtime 8.0 с официального сайта: https://dotnet.microsoft.com/download
Или измените TargetFramework во всех .csproj файлах проекта на установленную версию (например, net6.0-windows).

Пример вывода

После сканирования вы увидите:

Центральное управление драйверами

Сканировать сеть | [Статус: Найдено 1 устройство]

PC-01 (192.168.1.10)
  NVIDIA GeForce RTX 3060 — missing — [Установить]

Особенности

Минималистичный дизайн — современные карточки, тени, цвета.
MVVM — чистое разделение логики и представления.
SOLID — соблюдение принципов объектно-ориентированного программирования.
Асинхронность — UI не зависает во время сканирования.
Обработка ошибок — сообщения пользователю при возникновении проблем.

Лицензия

MIT License — свободное использование, модификация, распространение.

Авторы

[Жеребненко Дмитрий] — C# WPF, MVVM, UI Design
[Петров Дмитрий] — Python, сканирование сети
[Гордеев Алексей] — Python, поиск и установка драйверов

Поддержка

Если у вас возникли вопросы или проблемы — создайте issue в репозитории.

Заключение

DriverDrive — это готовое решение для централизованного управления драйверами в локальной сети.
Оно упрощает процесс обновления и установки драйверов, экономя время и усилия IT-специалистов.
