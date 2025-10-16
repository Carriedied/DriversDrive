using DriverDrive.Core.Models;

namespace DriverDrive.Core.Services
{
    public interface IDeviceScannerService
    {
        Task<IEnumerable<Computer>> ScanNetworkAsync();
    }
}
