using DriverDrive.Core.Models;
using DriverDrive.Core.Services;
using Newtonsoft.Json;
using System.Diagnostics;

namespace DriverDrive.Infrastructure.Services
{
    public class PythonExecutorService : IDeviceScannerService, IDriverInstallerService
    {
        private const string PYTHON_SCRIPT_PATH = @"C:\Users\Zhere\OneDrive\Документы\GitHub\DriversDrive\PythonScripts\driver_boost\driver_manager_api.py";

        public async Task<IEnumerable<Computer>> ScanNetworkAsync()
        {
            var request = new { command = "run_driver_scan_and_download", @params = new { } };
            var response = await ExecutePythonScriptAsync(request);

            if (response.status?.ToString() == "error")
                throw new InvalidOperationException($"Python error: {response.error?.ToString()}");

            var computers = new List<Computer>();

            foreach (dynamic comp in response.data)
            {
                var devices = new List<Device>();

                foreach (dynamic dev in comp.devices)
                {
                    devices.Add(new Device
                    {
                        Name = dev.name?.ToString(),
                        DriverStatus = Enum.Parse<DriverStatus>(dev.driver_status?.ToString(), true),
                        DriverUrl = dev.driver_url?.ToString()
                    });
                }

                computers.Add(new Computer
                {
                    IP = comp.ip?.ToString(),
                    Hostname = comp.hostname?.ToString(),
                    Devices = new System.Collections.ObjectModel.ObservableCollection<Device>(devices)
                });
            }

            return computers;
        }

        public async Task<bool> InstallDriverAsync(Device device, string computerIp)
        {
            var request = new
            {
                command = "install_driver",
                @params = new { device_name = device.Name, driver_url = device.DriverUrl, target_ip = computerIp }
            };

            var response = await ExecutePythonScriptAsync(request);

            return response.status?.ToString() == "success";
        }

        private async Task<dynamic> ExecutePythonScriptAsync(object request)
        {
            Console.WriteLine($"PythonExecutorService.ExecutePythonScriptAsync called with request: {request}");

            if (!File.Exists(PYTHON_SCRIPT_PATH))
            {
                throw new FileNotFoundException($"Python script not found at: {PYTHON_SCRIPT_PATH}");
            }

            using var process = new Process
            {
                StartInfo = new ProcessStartInfo
                {
                    FileName = "python",
                    Arguments = $"\"{PYTHON_SCRIPT_PATH}\"",
                    UseShellExecute = false,
                    RedirectStandardInput = true,
                    RedirectStandardOutput = true,
                    RedirectStandardError = true,
                    CreateNoWindow = true
                }
            };

            process.Start();

            var jsonRequest = JsonConvert.SerializeObject(request);

            await process.StandardInput.WriteLineAsync(jsonRequest);
            await process.StandardInput.FlushAsync();

            process.StandardInput.Close();

            var output = await process.StandardOutput.ReadToEndAsync();
            var error = await process.StandardError.ReadToEndAsync();

            //Console.WriteLine($"Python process started with PID: {process.Id}");
            //Console.WriteLine($"Python executable path (FileName): {process.StartInfo.FileName}");
            // Проверим, какой именно python вызывается
            //process.Start();
            //await process.StandardInput.WriteLineAsync("{\"command\":\"debug_python_version\", \"params\":{}}"); // Отправляем тестовую команду
            //await process.StandardInput.FlushAsync();
            //process.StandardInput.Close();

            // Ждем немного, чтобы процесс мог вывести версию
            //await Task.Delay(1000);

            //Console.WriteLine($"Python stdout: {output}");
            //Console.WriteLine($"Python stderr: {error}");

            if (!string.IsNullOrEmpty(error))
            {
                Console.WriteLine($"Python error: {error}");
                throw new Exception($"Python error: {error}");
            }

            Console.WriteLine($"Python output: {output}");

            return JsonConvert.DeserializeObject<dynamic>(output);
        }
    }
}
