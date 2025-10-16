using DriverDrive.Core.Models;

namespace DriverDrive.Core.Services
{
    public interface IDriverInstallerService
    {
        Task<bool> InstallDriverAsync(Device device, string computerIp);
    }
}
