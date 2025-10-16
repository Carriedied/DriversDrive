using DriverDrive.Infrastructure.Services;
using DriverDrive.ViewModel;
using Microsoft.Extensions.DependencyInjection;

using System.Windows;

namespace DriverDrive.App
{
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application
    {
        private IServiceProvider _serviceProvider = default!;

        protected override void OnStartup(StartupEventArgs e)
        {
            Console.WriteLine("App.OnStartup called"); // <--- Добавь это

            var services = new ServiceCollection();

            Console.WriteLine("Registering services..."); // <--- Добавь это
            services.AddSingleton<Core.Services.IDeviceScannerService, PythonExecutorService>();
            services.AddSingleton<Core.Services.IDriverInstallerService, PythonExecutorService>();
            services.AddTransient<MainViewModel>();
            services.AddTransient<MainWindow>();

            Console.WriteLine("Building service provider..."); // <--- Добавь это
            _serviceProvider = services.BuildServiceProvider();

            Console.WriteLine("Getting MainWindow..."); // <--- Добавь это
            var mainWindow = _serviceProvider.GetRequiredService<MainWindow>();
            Console.WriteLine("MainWindow retrieved, showing..."); // <--- Добавь это
            mainWindow.Show();
        }
    }
}
