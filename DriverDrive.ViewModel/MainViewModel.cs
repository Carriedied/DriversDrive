using System;
using System.Threading.Tasks;
using DriverDrive.Core.Common;
using DriverDrive.Core.Models;
using DriverDrive.Core.Services;
using DriverDrive.ViewModel.Common;
using System.Collections.ObjectModel;
using System.Windows.Input;

namespace DriverDrive.ViewModel
{
    public class MainViewModel : ObservableObject
    {
        private readonly IDeviceScannerService _scanner;
        private readonly IDriverInstallerService _installer;

        private ObservableCollection<Computer> _computers;
        private bool _isScanning;
        private string _statusMessage;

        public ObservableCollection<Computer> Computers
        {
            get => _computers;
            set => SetProperty(ref _computers, value);
        }

        public bool IsScanning
        {
            get => _isScanning;
            set => SetProperty(ref _isScanning, value);
        }

        public string StatusMessage
        {
            get => _statusMessage;
            set => SetProperty(ref _statusMessage, value);
        }

        public ICommand ScanCommand { get; }
        public ICommand InstallDriverCommand { get; }

        public MainViewModel(IDeviceScannerService scanner, IDriverInstallerService installer)
        {
            Console.WriteLine("MainViewModel constructor called");
            _scanner = scanner;
            _installer = installer;

            ScanCommand = new RelayCommand(async _ => await ScanNetworkAsync(), _ => !IsScanning);
            InstallDriverCommand = new RelayCommand(async param => await InstallDriverAsync((object[])param), param => !IsScanning);
        }

        private async Task ScanNetworkAsync()
        {
            Console.WriteLine("MainViewModel.ScanNetworkAsync called");
            IsScanning = true;
            StatusMessage = "Сканирование сети...";
            try
            {
                var computers = await _scanner.ScanNetworkAsync();
                Computers = new ObservableCollection<Computer>(computers);
                StatusMessage = $"Найдено {Computers.Count} устройств.";
            }
            catch (Exception ex)
            {
                StatusMessage = $"Ошибка: {ex.Message}";
            }
            finally
            {
                IsScanning = false;
            }
        }

        private async Task InstallDriverAsync(object[] parameters)
        {
            Console.WriteLine($"MainViewModel.InstallDriverAsync called with {parameters?.Length} parameters");
            if (parameters?.Length != 2) return;

            var device = parameters[0] as Device;
            var computerIp = parameters[1] as string;

            if (device == null || string.IsNullOrEmpty(computerIp))
            {
                StatusMessage = "Неверные параметры для установки драйвера.";
                return;
            }

            StatusMessage = $"Установка драйвера для {device.Name}...";
            try
            {
                var success = await _installer.InstallDriverAsync(device, computerIp);
                StatusMessage = success ? "Драйвер установлен." : "Ошибка установки.";
            }
            catch (Exception ex)
            {
                StatusMessage = $"Ошибка: {ex.Message}";
            }
        }
    }
}
