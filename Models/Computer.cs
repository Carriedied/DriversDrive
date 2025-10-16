using System.Collections.ObjectModel;
using DriversDrivers.Common;

namespace DriversDrivers.Models
{
    public class Computer : ObservableObject
    {
        private string _ip;
        private string _hostname;
        private ObservableCollection<Device> _devices;

        public string IP
        {
            get => _ip;
            set => SetProperty(ref _ip, value);
        }

        public string Hostname
        {
            get => _hostname;
            set => SetProperty(ref _hostname, value);
        }

        public ObservableCollection<Device> Devices
        {
            get => _devices;
            set => SetProperty(ref _devices, value);
        }
    }
}
