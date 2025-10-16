using DriversDrivers.Models;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace DriversDrivers.Interfaces
{
    public interface IDeviceScannerService
    {
        Task<IEnumerable<Computer>> ScanNetworkAsync();
    }
}
